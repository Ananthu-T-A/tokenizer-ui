const puppeteer = require('puppeteer');
const fs = require('fs');
const path = require('path');

(async () => {
  console.log('Starting E2E screenshot test...');

  const browser = await puppeteer.launch({
    headless: 'new',
    args: ['--no-sandbox', '--disable-setuid-sandbox']
  });

  const page = await browser.newPage();
  await page.setViewport({ width: 1200, height: 1000 });

  try {
    // Test 1: Text-only tokenization
    console.log('\n=== Test 1: Text-only tokenization ===');
    await page.goto('http://localhost:8080', { waitUntil: 'networkidle0' });
    await new Promise(r => setTimeout(r, 2000));

    // Select GPT-2 tokenizer
    await page.evaluate(() => {
      const select = document.getElementById('tokenizer-select');
      select.value = 'gpt2';
      select.dispatchEvent(new Event('change'));
    });

    await new Promise(r => setTimeout(r, 500));

    // Enter text
    await page.type('#text-input', 'Hello, world! This is a tokenizer visualization tool.');

    await new Promise(r => setTimeout(r, 2000));

    // Verify tokens are displayed
    const textTokenCount = await page.evaluate(() => {
      const output = document.getElementById('tokens-output');
      return output ? output.querySelectorAll('.token').length : 0;
    });

    console.log(`✓ Text tokens displayed: ${textTokenCount}`);
    if (textTokenCount === 0) {
      throw new Error('No tokens displayed for text-only mode');
    }

    // Take screenshot
    await page.screenshot({
      path: path.join(__dirname, '../test-output/screenshot-text.png'),
      fullPage: true
    });
    console.log('✓ Screenshot saved: test-output/screenshot-text.png');

    // Test 2: Multimodal tokenization
    console.log('\n=== Test 2: Multimodal tokenization ===');

    // Select Qwen2-VL
    await page.evaluate(() => {
      const select = document.getElementById('tokenizer-select');
      for (let i = 0; i < select.options.length; i++) {
        if (select.options[i].value.includes('Qwen2-VL')) {
          select.value = select.options[i].value;
          select.dispatchEvent(new Event('change'));
          break;
        }
      }
    });

    await new Promise(r => setTimeout(r, 500));

    // Switch to multimodal mode
    await page.evaluate(() => {
      const multimodalRadio = document.querySelector('input[value="multimodal"]');
      multimodalRadio.click();
    });

    await new Promise(r => setTimeout(r, 500));

    // Add text
    await page.evaluate(() => {
      const id = partIdCounter++;
      const part = { id, type: 'text', text: 'Hello, what\'s in a tokenizer visualization tool?' };
      contentParts.push(part);
      renderContentParts();
    });

    await new Promise(r => setTimeout(r, 500));

    // Add image
    const imagePath = path.join(__dirname, 'test-cat.jpg');
    let imageBuffer;

    // Download test image if it doesn't exist
    if (!fs.existsSync(imagePath)) {
      console.log('Downloading test image...');
      const https = require('https');
      imageBuffer = await new Promise((resolve, reject) => {
        https.get('https://cataas.com/cat', (res) => {
          const chunks = [];
          res.on('data', (chunk) => chunks.push(chunk));
          res.on('end', () => {
            const buffer = Buffer.concat(chunks);
            fs.writeFileSync(imagePath, buffer);
            resolve(buffer);
          });
          res.on('error', reject);
        });
      });
    } else {
      imageBuffer = fs.readFileSync(imagePath);
    }

    const base64Image = imageBuffer.toString('base64');
    const dataUrl = `data:image/jpeg;base64,${base64Image}`;

    await page.evaluate((dataUrl) => {
      const id = partIdCounter++;
      const part = { id, type: 'image', image: dataUrl };
      contentParts.push(part);
      renderContentParts();
      tokenizeContent();
    }, dataUrl);

    console.log('Waiting for tokenization...');

    // Wait for tokenization to complete (check for tokens output)
    let multimodalTokenCount = 0;
    for (let i = 0; i < 20; i++) {
      await new Promise(r => setTimeout(r, 1000));

      multimodalTokenCount = await page.evaluate(() => {
        const output = document.getElementById('tokens-output');
        if (!output) return 0;
        const tokens = output.querySelectorAll('.token');
        return tokens.length;
      });

      if (multimodalTokenCount > 0) {
        console.log(`✓ Tokenization complete after ${i + 1} seconds`);
        break;
      }
      console.log(`  Waiting for tokens... (${i + 1}/20)`);
    }

    if (multimodalTokenCount === 0) {
      throw new Error('No tokens displayed for multimodal mode after 20 seconds');
    }

    console.log(`✓ Multimodal tokens displayed: ${multimodalTokenCount}`);

    // Get actual token count from stats
    const totalTokens = await page.evaluate(() => {
      const stats = document.querySelector('.stats');
      if (!stats) return 0;
      const text = stats.textContent;
      const match = text.match(/(\d+)\s+tokens/);
      return match ? parseInt(match[1]) : 0;
    });
    console.log(`✓ Total token count: ${totalTokens}`);

    // Verify image tokens are grouped
    const hasImageGroup = await page.evaluate(() => {
      const output = document.getElementById('tokens-output');
      if (!output) return false;
      return output.textContent.includes('IMAGE') && output.textContent.includes('tokens');
    });

    console.log(`✓ Image tokens grouped: ${hasImageGroup}`);
    if (!hasImageGroup) {
      throw new Error('Image tokens not properly grouped');
    }

    // Scroll to show tokens output
    await page.evaluate(() => {
      const tokensOutput = document.getElementById('tokens-output');
      if (tokensOutput) {
        tokensOutput.scrollIntoView({ behavior: 'instant', block: 'end' });
      }
    });

    await new Promise(r => setTimeout(r, 500));

    // Take screenshot
    await page.screenshot({
      path: path.join(__dirname, '../test-output/screenshot-multimodal.png'),
      fullPage: true
    });
    console.log('✓ Screenshot saved: test-output/screenshot-multimodal.png');

    console.log('\n✅ All E2E tests passed!');
    await browser.close();
    process.exit(0);

  } catch (error) {
    console.error('\n❌ E2E test failed:', error.message);

    // Take error screenshot
    await page.screenshot({
      path: path.join(__dirname, '../test-output/screenshot-error.png'),
      fullPage: true
    });
    console.log('Error screenshot saved: test-output/screenshot-error.png');

    await browser.close();
    process.exit(1);
  }
})();

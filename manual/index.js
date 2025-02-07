const bsky = require('@atproto/api');
const fs = require('fs');
require('dotenv').config();

const config = JSON.parse(fs.readFileSync('manual/config.json', 'utf-8'));

const handles = {
    3: process.env.BSKY_HANDLE,
    4: process.env.BSKY_HANDLE2,
    5: process.env.BSKY_HANDLE3
};

const password = process.env.BSKY_PASSWORD;

async function uploadImageAndPost(letterCount) {
    if (!config[`${letterCount}_letter`]) {
        console.log(`Skipping ${letterCount}-letter image: No letters defined.`);
        return;
    }

    const { BskyAgent } = bsky;
    const agent = new BskyAgent({ service: 'https://bsky.social' });

    try {
        console.log(`Attempting login for ${letterCount}-letter account: ${handles[letterCount]}`);
        await agent.login({ identifier: handles[letterCount], password });

        const randomImagePath = `manual/random_image_${letterCount}.png`;
        const randomImage = fs.readFileSync(randomImagePath);
        const uploadResponse = await agent.uploadBlob(randomImage, { encoding: 'image/png' });

        if (!uploadResponse || !uploadResponse.data) {
            console.log(`Upload failed for ${letterCount}-letter image.`);
            return;
        }

        const randomLetters = config[`${letterCount}_letter`];
        const caption = `${letterCount} random letters (${randomLetters})`;

        const postResponse = await agent.post({
            text: caption,
            embed: {
                $type: 'app.bsky.embed.images',
                images: [{
                    image: uploadResponse.data.blob,
                    alt: `Random letters: ${randomLetters}
This image was generated automatically via a bot and pushed via a bot.
Automated repository can be found here: https://github.com/hutlaw/3rl`
                }]
            }
        });

        if (postResponse && postResponse.uri) {
            console.log(`Post created successfully for ${letterCount}-letter account: ${postResponse.uri}`);
        }
    } catch (error) {
        console.error(`Error posting for ${letterCount}-letter account:`, error);
    }
}

(async () => {
    for (const letterCount of [3, 4, 5]) {
        await uploadImageAndPost(letterCount);
    }
})();

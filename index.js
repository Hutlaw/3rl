const bsky = require('@atproto/api');
const fs = require('fs');
require('dotenv').config();

const handles = {
    3: process.env.BSKY_HANDLE,
    4: process.env.BSKY_HANDLE2,
    5: process.env.BSKY_HANDLE3
};

const password = process.env.BSKY_PASSWORD;

async function uploadImageAndPost(letterCount) {
    const { BskyAgent } = bsky;
    const agent = new BskyAgent({ service: 'https://bsky.social' });

    try {
        console.log(`Attempting login for ${letterCount} random letters with handle: ${handles[letterCount]}`);
        await agent.login({ identifier: handles[letterCount], password });

        const randomImagePath = `./random_image_${letterCount}.png`;
        const randomImage = fs.readFileSync(randomImagePath);
        const uploadResponse = await agent.uploadBlob(randomImage, { encoding: 'image/png' });

        if (!uploadResponse || !uploadResponse.data) return;

        const randomLetters = fs.readFileSync(`random_letters_${letterCount}.txt`, 'utf-8');
        const caption = `${letterCount} random letters (${randomLetters})`;

        const postResponse = await agent.post({
            text: caption,
            embed: {
                $type: 'app.bsky.embed.images',
                images: [{
                    image: uploadResponse.data.blob,
                    alt: `Random letters: ${randomLetters}`
                }]
            }
        });

        if (postResponse && postResponse.uri) {
            console.log(`Post created successfully for ${letterCount} random letters: ${postResponse.uri}`);
        }
    } catch (error) {
        console.error(`An error occurred for ${letterCount} random letters:`, error);
    }
}

(async () => {
    for (const letterCount of [3, 4, 5]) {
        await uploadImageAndPost(letterCount);
    }
})();

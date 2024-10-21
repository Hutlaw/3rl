const bsky = require('@atproto/api');
const fs = require('fs');
require('dotenv').config();

const handle = process.env.BSKY_HANDLE;
const password = process.env.BSKY_PASSWORD;
const randomImagePath = './random_image.png';

async function uploadImageAndPost() {
    const { BskyAgent } = bsky;
    const agent = new BskyAgent({ service: 'https://bsky.social' });

    try {
        await agent.login({ identifier: handle, password: password });
        console.log('Logged into Bluesky successfully.');

        const randomImage = fs.readFileSync(randomImagePath);
        const uploadResponse = await agent.uploadBlob(randomImage, { encoding: 'image/png' });

        if (!uploadResponse || !uploadResponse.data) {
            console.error('Image upload failed.');
            return;
        }

        console.log('Image uploaded successfully.');

        const randomLetters = process.argv[2] || 'XYZ';
        const caption = `3 random letters (${randomLetters[0]}, ${randomLetters[1]}, ${randomLetters[2]})`;

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
            console.log(`Post created successfully: ${postResponse.uri}`);
        } else {
            console.error('Post creation failed.');
        }

    } catch (error) {
        console.error('An error occurred:', error);
    }
}

uploadImageAndPost();

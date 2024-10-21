const { BskyAgent } = require('@atproto/api');
const fs = require('fs');
const path = require('path');
const { exec } = require('child_process');

async function generateImage() {
    return new Promise((resolve, reject) => {
        exec('python3 generate_image.py', (error, stdout, stderr) => {
            if (error) {
                console.error(`Error generating image: ${stderr}`);
                reject(stderr);
            } else {
                console.log(stdout);
                const lettersMatch = stdout.match(/Generated letters: (\w{3})/);
                if (lettersMatch) {
                    resolve(lettersMatch[1]);
                } else {
                    reject("Failed to extract letters from output.");
                }
            }
        });
    });
}

async function postImageWithCaption(randomLetters) {
    const agent = new BskyAgent({ service: 'https://bsky.social' });

    await agent.login({
        identifier: process.env.BSKY_HANDLE,
        password: process.env.BSKY_PASSWORD,
    });

    const imagePath = path.join(__dirname, 'random_image.png');
    const imageBytes = fs.readFileSync(imagePath);

    const uploadResponse = await agent.uploadBlob(imageBytes, {
        encoding: 'image/png',
    });

    const caption = `3 random letters (${randomLetters[0]}, ${randomLetters[1]}, ${randomLetters[2]})`;
    await agent.post({
        text: caption,
        embed: {
            $type: 'app.bsky.embed.images',
            images: [
                {
                    image: uploadResponse.data.blob,
                    alt: 'Random Image',
                },
            ],
        },
    });

    console.log('Image posted successfully with caption:', caption);
}

generateImage()
    .then(letters => postImageWithCaption(letters))
    .catch(error => console.error('Error:', error));

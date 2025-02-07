const bsky = require('@atproto/api');
const fs = require('fs');
const readline = require('readline');
require('dotenv').config();

const handles = {
    3: process.env.BSKY_HANDLE,
    4: process.env.BSKY_HANDLE2,
    5: process.env.BSKY_HANDLE3
};

const password = process.env.BSKY_PASSWORD;
const rl = readline.createInterface({ input: process.stdin, output: process.stdout });

async function uploadImageAndPost(letterCount, letters = null) {
    const { BskyAgent } = bsky;
    const agent = new BskyAgent({ service: 'https://bsky.social' });

    try {
        console.log(`Logging in for ${letterCount}-letter account...`);
        await agent.login({ identifier: handles[letterCount], password });

        const imgPath = `./random_image_${letterCount}.png`;
        const img = fs.readFileSync(imgPath);
        const uploadResponse = await agent.uploadBlob(img, { encoding: 'image/png' });

        if (!uploadResponse?.data) return;

        const text = letters || fs.readFileSync(`random_letters_${letterCount}.txt`, 'utf-8');
        const caption = `${letterCount} random letters (${text})`;

        const postResponse = await agent.post({
            text: caption,
            embed: {
                $type: 'app.bsky.embed.images',
                images: [{ image: uploadResponse.data.blob, alt: `Generated letters: ${text}` }]
            }
        });

        if (postResponse?.uri) console.log(`Post successful: ${postResponse.uri}`);
    } catch (error) {
        console.error(`Error posting for ${letterCount} letters:`, error);
    }
}

(async () => {
    if (process.argv[2] === "manual") {
        rl.question("Use custom letters? (yes/no): ", (useCustom) => {
            if (useCustom.toLowerCase() !== "yes") return rl.close();
            rl.question("Select account (3, 4, 5): ", (account) => {
                if (!["3", "4", "5"].includes(account)) return rl.close();
                rl.question(`Enter ${account} letters: `, (letters) => {
                    if (letters.length !== parseInt(account)) return rl.close();
                    uploadImageAndPost(parseInt(account), letters);
                    rl.close();
                });
            });
        });
    } else {
        [3, 4, 5].forEach(uploadImageAndPost);
    }
})();
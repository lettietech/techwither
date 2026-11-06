export default async function handler(req, res) {
    // 1. Security Check: Only allow POST requests from your website
    if (req.method !== 'POST') {
        return res.status(405).json({ error: 'Method not allowed' });
    }

    // 2. Grab the prompt sent from your frontend JavaScript widget
    const { prompt } = req.body;
    if (!prompt) {
        return res.status(400).json({ error: 'Prompt is required' });
    }

    try {
        // 3. Securely pull your API key from environment variables (hidden from public users)
        const apiKey = process.env.AI_API_KEY; 
        if (!apiKey) {
            throw new Error('AI API key is missing on the server backend.');
        }

        // 4. Server-to-server fetch request to the AI model provider
        const aiResponse = await fetch('https://api.openai.com/v1/chat/completions', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'Authorization': `Bearer ${apiKey}`
            },
            body: JSON.stringify({
                model: 'gpt-4o-mini',
                messages: [{ role: 'user', content: prompt }],
                temperature: 0.7
            })
        });

        const data = await aiResponse.json();
        
        if (data.error) {
            throw new Error(data.error.message);
        }

        const answer = data.choices[0].message.content;

        // 5. Send the real answer safely back to your website frontend
        return res.status(200).json({ answer: answer });

    } catch (error) {
        return res.status(500).json({ error: error.message });
    }
}
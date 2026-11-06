exports.handler = async function(event, context) {
    // 1. Security Check: Only allow POST requests
    if (event.httpMethod !== 'POST') {
        return { 
            statusCode: 405, 
            body: JSON.stringify({ error: 'Method not allowed' }) 
        };
    }

    try {
        const { prompt } = JSON.parse(event.body);
        if (!prompt) {
            return { 
                statusCode: 400, 
                body: JSON.stringify({ error: 'Prompt is required' }) 
            };
        }

        // 2. Securely grab your API key from Netlify Environment Variables
        const apiKey = process.env.AI_API_KEY;
        if (!apiKey) {
            throw new Error('AI API key is missing on the Netlify server.');
        }

        // 3. Call OpenAI API securely from the server side
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

        // 4. Return response back to your website frontend
        return {
            statusCode: 200,
            body: JSON.stringify({ answer: answer })
        };

    } catch (error) {
        return {
            statusCode: 500,
            body: JSON.stringify({ error: error.message })
        };
    }
};
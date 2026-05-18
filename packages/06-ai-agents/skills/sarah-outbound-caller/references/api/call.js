const VAPI_API_KEY = process.env.VAPI_API_KEY;
const DEFAULT_ASSISTANT_ID = "2e7609a1-dcfd-430e-9111-1426cb3cb38e"; // Sarah
const PHONE_NUMBER_ID = "921f17a9-1924-44b9-a0b2-def45ffff852";

export default async function handler(req, res) {
    if (req.method !== 'POST') {
        return res.status(405).json({ error: 'Method not allowed' });
    }

    const { name, phone, address, message, assistantId, type } = req.body;
    const targetAssistantId = assistantId || DEFAULT_ASSISTANT_ID;
    const firstName = name ? name.split(' ')[0] : 'there';
    
    // Format address for natural speech (SSML-friendly)
    const spokenAddress = address ? formatAddressForSpeech(address) : null;
    
    // Logic for custom reminder vs standard Sarah lead gen
    let firstMessage = "";
    if (message) {
        if (type === 'rdm') {
            firstMessage = `Hi ${firstName}, this is Sarah, the personal AI assistant for Tammie and Charles at the Real Deal Meetup. Charles asked me to give you a quick update: ${message}. See you soon!`;
        } else if (type === 'mms') {
            firstMessage = `Hi ${firstName}, this is Sarah, the personal AI assistant for Tammie and Charles at Mad Marketing Success. I'm calling because Charles has a custom message for you: ${message}. Let me know if you're interested!`;
        } else {
            // Default to Skool style if type not specified but message exists
            firstMessage = `Hi ${firstName}, this is Sarah, the personal AI assistant for Tammie and Charles at the REI AI Skool Community. Charles wanted me to reach out and remind you: ${message}. Thanks, and have a great day!`;
        }
    } else {
        // Standard Sarah script for Acquisitions - mention address if provided
        if (spokenAddress) {
            firstMessage = `Hi can I speak with ${firstName}, this is Sarah, the personal AI assistant for Tammie and Charles calling from Chucky Buys Lucky Houses. I'm calling about your property at ${spokenAddress}.`;
        } else {
            firstMessage = `Hi can I speak with ${firstName}, this is Sarah, the personal AI assistant for Tammie and Charles calling from Chucky Buys Lucky Houses.`;
        }
    }

    try {
        const response = await fetch('https://api.vapi.ai/call', {
            method: 'POST',
            headers: {
                'Authorization': `Bearer ${VAPI_API_KEY}`,
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                assistantId: targetAssistantId,
                phoneNumberId: PHONE_NUMBER_ID,
                customer: {
                    number: phone,
                    name: name
                },
                assistantOverrides: {
                    firstMessage: firstMessage,
                    variableValues: {
                        "first_name": firstName,
                        "property_address": spokenAddress || address || 'your property',
                        "raw_address": address || ''
                    }
                }
            })
        });

        const data = await response.json();
        return res.status(200).json(data);
    } catch (error) {
        return res.status(500).json({ error: error.message });
    }
}

/**
 * Format address for natural speech
 * Example: "1234 Main St NW" → "1234 Main Street Northwest"
 * Helps TTS pronounce addresses correctly
 */
function formatAddressForSpeech(address) {
    if (!address) return '';
    
    let formatted = address.trim();
    
    // Expand common abbreviations (with word boundaries to avoid double-replace)
    const replacements = {
        '\\bSt\\b': 'Street',
        '\\bSt\\.': 'Street',
        '\\bAve\\b': 'Avenue',
        '\\bAve\\.': 'Avenue',
        '\\bRd\\b': 'Road',
        '\\bRd\\.': 'Road',
        '\\bBlvd\\b': 'Boulevard',
        '\\bBlvd\\.': 'Boulevard',
        '\\bDr\\b': 'Drive',
        '\\bDr\\.': 'Drive',
        '\\bLn\\b': 'Lane',
        '\\bLn\\.': 'Lane',
        '\\bCt\\b': 'Court',
        '\\bCt\\.': 'Court',
        '\\bPl\\b': 'Place',
        '\\bPl\\.': 'Place',
        '\\bCir\\b': 'Circle',
        '\\bCir\\.': 'Circle',
        '\\bNW\\b': 'Northwest',
        '\\bNE\\b': 'Northeast',
        '\\bSW\\b': 'Southwest',
        '\\bSE\\b': 'Southeast',
        '\\bN\\b': 'North',
        '\\bS\\b': 'South',
        '\\bE\\b': 'East',
        '\\bW\\b': 'West',
    };
    
    for (const [pattern, replacement] of Object.entries(replacements)) {
        formatted = formatted.replace(new RegExp(pattern, 'gi'), replacement);
    }
    
    // Clean up multiple spaces
    formatted = formatted.replace(/\s+/g, ' ');
    
    return formatted.trim();
}

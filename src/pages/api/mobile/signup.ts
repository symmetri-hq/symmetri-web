// src/pages/api/mobile/signup.ts
// Mobile-specific signup endpoint acting strictly as a proxy to FastAPI
import type { NextApiRequest, NextApiResponse } from 'next';
import jwt from 'jsonwebtoken';

type ApiError = { error: string; message?: string };
type ApiSuccess = { token: string; user: any };

function generateToken(user: any): string {
    const secret = process.env.JWT_SECRET;
    if (!secret) throw new Error('JWT_SECRET is not set');
    return jwt.sign(
        {
            userId: user.id,
            email: user.email,
            symmetriId: user.symmetri_id
        },
        secret,
        { expiresIn: '7d' }
    );
}

export default async function handler(req: NextApiRequest, res: NextApiResponse<ApiSuccess | ApiError>) {
    if (req.method !== 'POST') {
        return res.status(405).json({ error: 'Method not allowed' });
    }

    const { email, password, firstName, lastName, country, phone, dob } = req.body || {};

    try {
        const fastapiUrl = process.env.FASTAPI_URL || 'https://symmetri-api.onrender.com';
        
        // Forward request to FastAPI
        const response = await fetch(`${fastapiUrl}/api/auth/signup`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                first_name: firstName,
                last_name: lastName,
                email: email,
                password: password,
                country_of_residence: country || 'US',
                country_destiny: 'MX',
                dob: dob || '1990-01-01',
                phone: phone
            }),
        });

        const data = await response.json();

        if (!response.ok) {
            return res.status(response.status).json({
                error: data.message || data.detail || 'Error from backend',
                message: JSON.stringify(data)
            });
        }

        // FastAPI successfully created the user. Let's create a token for them.
        const token = generateToken(data.user || data);

        return res.status(201).json({
            token,
            user: data.user || data
        });
    } catch (error: any) {
        return res.status(500).json({ error: 'Server error', message: error.message });
    }
}

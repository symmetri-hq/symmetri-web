import { jwtVerify } from 'jose';
import { TruequeSession } from '../types/auth';

const SECRET_KEY = process.env.SESSION_SECRET || 'default_local_secret_change_me_in_prod';
const key = new TextEncoder().encode(SECRET_KEY);

export async function decrypt(input: string): Promise<TruequeSession | null> {
  try {
    const { payload } = await jwtVerify(input, key, { algorithms: ['HS256'] });
    return payload as unknown as TruequeSession;
  } catch (error) {
    return null;
  }
}

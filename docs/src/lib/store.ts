import { writable } from 'svelte/store';

export const selectedProvider = writable<string>('');
export const selectedEndpoint = writable<string>('');
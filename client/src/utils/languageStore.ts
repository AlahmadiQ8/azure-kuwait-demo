/**
 * Svelte store for managing language state reactively across components
 */

import { writable } from 'svelte/store';
import { getDefaultLanguage, saveLanguagePreference, type Language } from './i18n.js';

// Create a reactive language store
export const currentLanguage = writable<Language>(getDefaultLanguage());

// Function to change language and persist it
export function setLanguage(language: Language): void {
  currentLanguage.set(language);
  saveLanguagePreference(language);
}
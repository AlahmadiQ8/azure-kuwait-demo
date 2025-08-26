<!--
Language switcher component for switching between English and Arabic
-->
<script lang="ts">
    import { currentLanguage, setLanguage } from '../utils/languageStore.js';
    import type { Language } from '../utils/i18n.js';
    
    let isOpen = false;
    
    function toggleDropdown() {
        isOpen = !isOpen;
    }
    
    function selectLanguage(language: Language) {
        setLanguage(language);
        isOpen = false;
        
        // Update document attributes for RTL support
        if (typeof window !== 'undefined') {
            document.documentElement.setAttribute('data-lang', language);
            document.documentElement.setAttribute('lang', language);
            
            // Dispatch custom event for other components to react
            window.dispatchEvent(new CustomEvent('app:languagechange'));
        }
    }
    
    // Close dropdown when clicking outside
    function handleClickOutside(event: MouseEvent) {
        const target = event.target as Element;
        if (!target.closest('.language-switcher')) {
            isOpen = false;
        }
    }
    
    $: if (typeof window !== 'undefined') {
        if (isOpen) {
            window.addEventListener('click', handleClickOutside);
        } else {
            window.removeEventListener('click', handleClickOutside);
        }
    }
    
    $: currentLangDisplay = $currentLanguage === 'en' ? 'EN' : 'عر';
</script>

<div class="language-switcher relative inline-block">
    <button
        on:click={toggleDropdown}
        class="flex items-center px-3 py-2 text-sm font-medium text-white hover:text-blue-200 transition-colors duration-300 focus:outline-none focus:ring-2 focus:ring-blue-400 focus:ring-opacity-50 rounded"
        aria-label="Change language"
    >
        <svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4 mr-1" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M3 5h12M9 3v2m1.048 9.5A18.022 18.022 0 016.412 9m6.088 9h7M11 21l5-10 5 10M12.751 5C11.783 10.77 8.07 15.61 3 18.129" />
        </svg>
        {currentLangDisplay}
        <svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4 ml-1 transition-transform duration-200" class:rotate-180={isOpen} fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 9l-7 7-7-7" />
        </svg>
    </button>
    
    {#if isOpen}
        <div class="absolute right-0 mt-2 w-32 bg-white dark:bg-slate-800 text-slate-800 dark:text-white rounded-lg shadow-lg border border-slate-200 dark:border-slate-700 z-20 transition-colors duration-300">
            <div class="py-1">
                <button
                    on:click={() => selectLanguage('en')}
                    class="block w-full text-left px-4 py-2 hover:bg-slate-100 dark:hover:bg-slate-700 transition-colors duration-200"
                    class:bg-blue-50={$currentLanguage === 'en'}
                    class:dark:bg-blue-900={$currentLanguage === 'en'}
                    class:text-blue-600={$currentLanguage === 'en'}
                    class:dark:text-blue-400={$currentLanguage === 'en'}
                >
                    <span class="flex items-center">
                        <span class="mr-2">🇺🇸</span>
                        English
                    </span>
                </button>
                <button
                    on:click={() => selectLanguage('ar')}
                    class="block w-full text-left px-4 py-2 hover:bg-slate-100 dark:hover:bg-slate-700 transition-colors duration-200"
                    class:bg-blue-50={$currentLanguage === 'ar'}
                    class:dark:bg-blue-900={$currentLanguage === 'ar'}
                    class:text-blue-600={$currentLanguage === 'ar'}
                    class:dark:text-blue-400={$currentLanguage === 'ar'}
                >
                    <span class="flex items-center">
                        <span class="mr-2">🇰🇼</span>
                        العربية
                    </span>
                </button>
            </div>
        </div>
    {/if}
</div>

<style>
    .rotate-180 {
        transform: rotate(180deg);
    }
</style>
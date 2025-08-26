/**
 * Simple internationalization utility for Kuwait Fine Dining app
 * Supports English and Arabic with RTL text direction
 */

export type Language = 'en' | 'ar';

export interface Translation {
  // Site basics
  siteTitle: string;
  welcome: string;
  welcomeSubtext: string;
  
  // Navigation
  home: string;
  about: string;
  
  // Restaurant list
  featuredRestaurants: string;
  viewDetails: string;
  noRestaurantsAvailable: string;
  
  // About page
  aboutTitle: string;
  aboutDescription1: string;
  aboutDescription2: string;
  backToRestaurants: string;
  
  // Loading and errors
  loading: string;
  error: string;
}

export const translations: Record<Language, Translation> = {
  en: {
    siteTitle: 'Kuwait Fine Dining',
    welcome: 'Welcome to Kuwait Fine Dining',
    welcomeSubtext: 'Find your next restaurant in Kuwait!',
    
    home: 'Home',
    about: 'About',
    
    featuredRestaurants: 'Featured Restaurants',
    viewDetails: 'View details',
    noRestaurantsAvailable: 'No restaurants available at the moment.',
    
    aboutTitle: 'About Kuwait Fine Dining',
    aboutDescription1: 'Kuwait Fine Dining is a restaurant directory for Kuwait with a culinary theme.',
    aboutDescription2: 'It highlights local dining spots ranging from traditional Kuwaiti kitchens to modern fusion concepts. Each listing showcases the restaurant\'s specialties, atmosphere, and story—making it easy to explore, compare, and discover great places to eat across Kuwait.',
    backToRestaurants: 'Back to Restaurants',
    
    loading: 'Loading...',
    error: 'Error'
  },
  ar: {
    siteTitle: 'مطاعم الكويت الفاخرة',
    welcome: 'مرحباً بكم في مطاعم الكويت الفاخرة',
    welcomeSubtext: 'اعثر على مطعمك القادم في الكويت!',
    
    home: 'الرئيسية',
    about: 'حول',
    
    featuredRestaurants: 'المطاعم المميزة',
    viewDetails: 'عرض التفاصيل',
    noRestaurantsAvailable: 'لا توجد مطاعم متاحة في الوقت الحالي.',
    
    aboutTitle: 'حول مطاعم الكويت الفاخرة',
    aboutDescription1: 'مطاعم الكويت الفاخرة هو دليل مطاعم للكويت مع طابع الطهي.',
    aboutDescription2: 'يسلط الضوء على أماكن تناول الطعام المحلية التي تتراوح من المطابخ الكويتية التقليدية إلى مفاهيم الاندماج الحديثة. تعرض كل قائمة تخصصات المطعم وأجوائه وقصته - مما يجعل من السهل استكشاف ومقارنة واكتشاف أماكن رائعة لتناول الطعام في جميع أنحاء الكويت.',
    backToRestaurants: 'العودة إلى المطاعم',
    
    loading: 'جاري التحميل...',
    error: 'خطأ'
  }
};

export const isRTL = (language: Language): boolean => language === 'ar';

/**
 * Get translation for a key in the specified language
 */
export function getTranslation(language: Language, key: keyof Translation): string {
  return translations[language][key];
}

/**
 * Get the default language from browser or fallback to English
 */
export function getDefaultLanguage(): Language {
  if (typeof window === 'undefined') {
    return 'en'; // Default for SSR
  }
  
  // Check localStorage first
  const stored = localStorage.getItem('preferred-language') as Language;
  if (stored && (stored === 'en' || stored === 'ar')) {
    return stored;
  }
  
  // Check browser language
  const browserLang = navigator.language.toLowerCase();
  if (browserLang.startsWith('ar')) {
    return 'ar';
  }
  
  return 'en';
}

/**
 * Save language preference to localStorage
 */
export function saveLanguagePreference(language: Language): void {
  if (typeof window !== 'undefined') {
    localStorage.setItem('preferred-language', language);
  }
}
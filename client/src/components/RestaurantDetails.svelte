<script lang="ts">
    import { onMount } from "svelte";
    
    interface Restaurant {
        id: number;
        title: string;
        description: string;
        publisher: {
            id: number;
            name: string;
        } | null;
        category: {
            id: number;
            name: string;
        } | null;
        starRating: number | null;
    }

    // Accept either a restaurant object or a restaurantId
    export let restaurant: Restaurant | undefined = undefined;
    export let restaurantId = 0;
    
    let loading = true;
    let error: string | null = null;
    let restaurantData: Restaurant | null = null;
    
    onMount(async () => {
        // If restaurant object is provided directly, use it
        if (restaurant) {
            restaurantData = restaurant;
            loading = false;
            return;
        }
        
        // Otherwise fetch data using restaurantId
        if (restaurantId) {
            try {
                const response = await fetch(`/api/restaurants/${restaurantId}`);
                if (response.ok) {
                    restaurantData = await response.json();
                } else {
                    error = `Failed to fetch restaurant: ${response.status} ${response.statusText}`;
                }
            } catch (err) {
                error = `Error: ${err instanceof Error ? err.message : String(err)}`;
            } finally {
                loading = false;
            }
        } else {
            error = "No restaurant ID provided";
            loading = false;
        }
    });

    // Function to render stars based on rating
    function renderStarRating(rating: number | null): string {
        if (rating === null) return "Not yet rated";
        
        const fullStars = Math.floor(rating);
        const halfStar = rating % 1 >= 0.5;
        const emptyStars = 5 - fullStars - (halfStar ? 1 : 0);
        
        return '★'.repeat(fullStars) + (halfStar ? '½' : '') + '☆'.repeat(emptyStars);
    }
</script>

{#if loading}
    <div class="animate-pulse bg-slate-800/60 backdrop-blur-sm rounded-xl overflow-hidden p-6">
        <div class="h-8 bg-slate-700 rounded w-1/2 mb-6"></div>
        <div class="h-4 bg-slate-700 rounded w-3/4 mb-3"></div>
        <div class="h-4 bg-slate-700 rounded w-1/2 mb-3"></div>
        <div class="h-4 bg-slate-700 rounded w-full mb-3"></div>
    </div>
{:else if error}
    <div class="bg-red-500/20 border border-red-500/50 text-red-400 rounded-xl p-6">
        {error}
    </div>
{:else if restaurantData}
    <div class="bg-slate-800/70 backdrop-blur-sm border border-slate-700 rounded-xl overflow-hidden" data-testid="restaurant-details">
        <div class="p-6">
            <div class="flex justify-between items-start flex-wrap gap-3">
                <h1 class="text-3xl font-bold text-slate-100 mb-2" data-testid="restaurant-details-title">{restaurantData.title}</h1>
                
                {#if restaurantData.starRating !== null}
                <div class="flex items-center">
                    <span class="bg-blue-500/20 text-blue-400 text-sm px-3 py-1 rounded-full" data-testid="restaurant-rating">
                        <span class="text-yellow-400">{renderStarRating(restaurantData.starRating)}</span> 
                        {restaurantData.starRating.toFixed(1)}
                    </span>
                </div>
                {/if}
            </div>
            
            <div class="flex flex-wrap gap-2 mt-4 mb-6">
                {#if restaurantData.category}
                    <span class="text-xs font-medium px-2.5 py-0.5 rounded bg-blue-900/60 text-blue-300" data-testid="restaurant-details-category">
                        {restaurantData.category.name}
                    </span>
                {/if}
                {#if restaurantData.publisher}
                    <span class="text-xs font-medium px-2.5 py-0.5 rounded bg-purple-900/60 text-purple-300" data-testid="restaurant-details-publisher">
                        {restaurantData.publisher.name}
                    </span>
                {/if}
            </div>
            
            <div class="space-y-4 mt-6">
                <h2 class="text-lg font-semibold text-slate-200 mb-2">About this restaurant</h2>
                <div class="text-slate-400 space-y-4">
                    <p data-testid="restaurant-details-description">{restaurantData.description}</p>
                </div>
            </div>
            
            <div class="mt-8">
                <button class="w-full bg-gradient-to-r from-blue-600 to-purple-600 hover:from-blue-500 hover:to-purple-500 text-white font-medium py-3 px-4 rounded-lg transition-all duration-200 flex justify-center items-center" data-testid="back-restaurant-button">
                    <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5 mr-2" viewBox="0 0 20 20" fill="currentColor">
                        <path fill-rule="evenodd" d="M3.172 5.172a4 4 0 015.656 0L10 6.343l1.172-1.171a4 4 0 115.656 5.656L10 17.657l-6.828-6.829a4 4 0 010-5.656z" clip-rule="evenodd" />
                    </svg>
                    Save to favorites
                </button>
            </div>
        </div>
    </div>
{:else}
    <div class="bg-slate-800/60 backdrop-blur-sm rounded-xl p-6">
        <p class="text-slate-400">No restaurant information available</p>
    </div>
{/if}
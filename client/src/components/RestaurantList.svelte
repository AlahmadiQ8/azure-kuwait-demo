<script lang="ts">
    import { onMount } from "svelte";

    interface Restaurant {
        id: number;
        title: string;
        description: string;
        publisher?: {
            id: number;
            name: string;
        };
        category?: {
            id: number;
            name: string;
        };
        starRating?: number;
    }

    interface Category {
        id: number;
        name: string;
    }

    export let restaurants: Restaurant[] = [];
    let loading = true;
    let error: string | null = null;
    let selectedCategory: string = '';
    let availableCategories: Category[] = [];

    const fetchRestaurants = async (categoryFilter?: string) => {
        loading = true;
        try {
            const url = categoryFilter 
                ? `/api/restaurants?category=${encodeURIComponent(categoryFilter)}`
                : '/api/restaurants';
            const response = await fetch(url);
            if(response.ok) {
                restaurants = await response.json();
            } else {
                error = `Failed to fetch data: ${response.status} ${response.statusText}`;
            }
        } catch (err) {
            error = `Error: ${err instanceof Error ? err.message : String(err)}`;
        } finally {
            loading = false;
        }
    };

    const fetchCategories = async () => {
        try {
            // First, get all restaurants to extract unique categories
            const response = await fetch('/api/restaurants');
            if(response.ok) {
                const allRestaurants: Restaurant[] = await response.json();
                const categoryMap = new Map<number, Category>();
                
                allRestaurants.forEach(restaurant => {
                    if (restaurant.category) {
                        categoryMap.set(restaurant.category.id, restaurant.category);
                    }
                });
                
                availableCategories = Array.from(categoryMap.values())
                    .sort((a, b) => a.name.localeCompare(b.name));
            }
        } catch (err) {
            console.error('Error fetching categories:', err);
        }
    };

    const handleCategoryChange = async (event: Event) => {
        const target = event.target as HTMLSelectElement;
        selectedCategory = target.value;
        
        if (selectedCategory === '') {
            await fetchRestaurants();
        } else {
            await fetchRestaurants(selectedCategory);
        }
    };

    onMount(() => {
        fetchCategories();
        fetchRestaurants();
    });
</script>

<div>
    <h2 class="text-2xl font-medium mb-6 text-slate-100">Featured Restaurants</h2>
    
    <!-- Category Filter -->
    <div class="mb-6">
        <label for="category-filter" class="block text-sm font-medium text-slate-300 mb-2">
            Filter by Category
        </label>
        <select 
            id="category-filter"
            bind:value={selectedCategory}
            on:change={handleCategoryChange}
            class="w-full md:w-auto px-4 py-2 bg-slate-800/60 border border-slate-700 rounded-xl text-slate-100 focus:ring-2 focus:ring-blue-500 focus:border-transparent transition-colors"
            data-testid="category-filter"
        >
            <option value="">All Categories</option>
            {#each availableCategories as category}
                <option value={category.id}>{category.name}</option>
            {/each}
        </select>
    </div>
    
    {#if loading}
        <!-- loading animation -->
        <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-6">
            {#each Array(6) as _, i}
                <div class="bg-slate-800/60 backdrop-blur-sm rounded-xl overflow-hidden shadow-lg border border-slate-700/50">
                    <div class="p-6">
                        <div class="animate-pulse">
                            <div class="h-6 bg-slate-700 rounded w-3/4 mb-3"></div>
                            <div class="h-4 bg-slate-700 rounded w-1/2 mb-4"></div>
                            <div class="h-3 bg-slate-700 rounded w-full mb-3"></div>
                            <div class="h-3 bg-slate-700 rounded w-5/6 mb-4"></div>
                            <div class="h-2 bg-slate-700 rounded-full w-full mb-2"></div>
                            <div class="h-4 bg-slate-700 rounded w-1/4 mt-4"></div>
                        </div>
                    </div>
                </div>
            {/each}
        </div>
    {:else if error}
        <!-- error display -->
        <div class="text-center py-12 bg-slate-800/50 backdrop-blur-sm rounded-xl border border-slate-700">
            <p class="text-red-400">{error}</p>
        </div>
    {:else if restaurants.length === 0}
        <!-- no restaurants found -->
        <div class="text-center py-12 bg-slate-800/50 backdrop-blur-sm rounded-xl border border-slate-700">
            <p class="text-slate-300">No restaurants available at the moment.</p>
        </div>
    {:else}
        <!-- restaurant list -->
        <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-6" data-testid="restaurants-grid">
            {#each restaurants as restaurant (restaurant.id)}
                <a 
                    href={`/restaurant/${restaurant.id}`} 
                    class="group block bg-slate-800/60 backdrop-blur-sm rounded-xl overflow-hidden shadow-lg border border-slate-700/50 hover:border-blue-500/50 hover:shadow-blue-500/10 hover:shadow-xl transition-all duration-300 hover:translate-y-[-6px]"
                    data-testid="restaurant-card"
                    data-restaurant-id={restaurant.id}
                    data-restaurant-title={restaurant.title}
                >
                    <div class="p-6 relative">
                        <div class="absolute inset-0 bg-gradient-to-r from-blue-600/10 to-purple-600/5 opacity-0 group-hover:opacity-100 transition-opacity duration-300"></div>
                        <div class="relative z-10">
                            <h3 class="text-xl font-semibold text-slate-100 mb-2 group-hover:text-blue-400 transition-colors" data-testid="restaurant-title">{restaurant.title}</h3>
                            
                            {#if restaurant.category || restaurant.publisher}
                                <div class="flex gap-2 mb-3">
                                    {#if restaurant.category}
                                        <span class="text-xs font-medium px-2.5 py-0.5 rounded bg-blue-900/60 text-blue-300" data-testid="restaurant-category">
                                            {restaurant.category.name}
                                        </span>
                                    {/if}
                                    {#if restaurant.publisher}
                                        <span class="text-xs font-medium px-2.5 py-0.5 rounded bg-purple-900/60 text-purple-300" data-testid="restaurant-publisher">
                                            {restaurant.publisher.name}
                                        </span>
                                    {/if}
                                </div>
                            {/if}
                            
                            <p class="text-slate-400 mb-4 text-sm line-clamp-2" data-testid="restaurant-description">{restaurant.description}</p>
                            
                            <div class="mt-4 text-sm text-blue-400 font-medium flex items-center">
                                <span>View details</span>
                                <svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4 ml-1 transform transition-transform duration-300 group-hover:translate-x-2" viewBox="0 0 20 20" fill="currentColor">
                                    <path fill-rule="evenodd" d="M12.293 5.293a1 1 0 011.414 0l4 4a1 1 0 010 1.414l-4 4a1 1 0 01-1.414-1.414L14.586 11H3a1 1 0 110-2h11.586l-2.293-2.293a1 1 0 010-1.414z" clip-rule="evenodd" />
                                </svg>
                            </div>
                        </div>
                    </div>
                </a>
            {/each}
        </div>
    {/if}
</div>
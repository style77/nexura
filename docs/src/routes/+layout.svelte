<script lang="ts">
  import "../app.css";
  import { onMount } from "svelte";
  import docs from "../docs.json";
  import { selectedProvider, selectedEndpoint } from '$lib/store';

  let expandedProviders: Record<string, boolean> = {};

  function toggleProvider(providerName: string) {
    expandedProviders[providerName] = !expandedProviders[providerName];
  }

  function getEndpoints(providerName: string) {
    return docs[providerName]?.endpoints || { error: "No endpoints found" };
  }

  onMount(() => {
    Object.keys(docs).forEach((providerName) => {
      expandedProviders[providerName] = false;
    });
  });

  function handleProviderSelect(providerName: string) {
    selectedProvider.set(providerName);
    selectedEndpoint.set(''); // Clear endpoint selection when provider changes
  }

  function handleEndpointSelect(providerName: string, endpointName: string) {
    selectedProvider.set(providerName);
    selectedEndpoint.set(endpointName);
  }
</script>

<div class="flex h-full bg-gray-100">
  <aside class="fixed top-0 left-0 w-64 bg-gray-800 text-white transition-transform transform translate-x-0 h-full">
    <div class="p-4">
      <button class="text-white focus:outline-none">
        <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 6h16M4 12h16M4 18h16"></path>
        </svg>
      </button>
      <nav class="mt-6">
        <ul>
          {#each Object.entries(docs) as [providerName, provider]}
            <li>
              <a href="#" class="py-2 px-4 hover:bg-gray-700 w-full rounded flex flex-row items-center justify-between z-[5]" on:click={() => handleProviderSelect(providerName)}>
                {provider.name}
                <button class="cursor-pointer z-10" on:click={() => toggleProvider(providerName)}>
                  <svg class={`w-4 h-4 transform transition-transform ${expandedProviders[providerName] ? "rotate-180" : ""}`} fill="none" stroke="currentColor" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 9l-7 7-7-7"/>
                  </svg>
                </button>
              </a>
              {#if expandedProviders[providerName]}
                <ul class="ml-4 mt-2">
                  {#each Object.entries(getEndpoints(providerName)) as [endpointName, endpoint]}
                    {#if endpoint.error}
                      <li>
                        <p class="py-2 px-4 text-red-500">{endpoint.error}</p>
                      </li>
                    {:else}
                      <li>
                        <a href="#" class="block py-1.5 px-4 hover:bg-gray-700 text-sm text-gray-400 rounded {selectedEndpoint === endpointName ? 'bg-gray-700' : ''}" on:click={() => handleEndpointSelect(providerName, endpointName)}>
                          {endpoint.name}
                        </a>
                      </li>
                    {/if}
                  {/each}
                </ul>
              {/if}
            </li>
          {/each}
        </ul>
      </nav>
    </div>
  </aside>

  <div class="flex-1 flex flex-col ml-64">
    <header class="bg-gray-800 text-white p-4">
      <h1 class="text-xl font-semibold">Documentation</h1>
    </header>

    <main class="p-6">
      <slot></slot>
    </main>
  </div>
</div>

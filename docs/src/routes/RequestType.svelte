<script lang="ts">
  import SvelteMarkdown from 'svelte-markdown'
  import AvailableValues from './AvailableValues.svelte';

  export let data: any[]; // Expecting an array of request type objects
  let expandedIndex: number | null = 0; // Index of the expanded request type

  function convertNewlinesToBr(text: string): string {
    return text.replace(/\n/g, '');
  }
</script>

<div class="flex flex-col gap-6">
  {#each data as item}
    <div class="flex flex-col">
      <div class="flex flex-row items-center">
        <!-- Badge for Disabled and Beta -->
        <div class="flex flex-row items-center">
          {#if item.disabled}
            <div>
              <span class="bg-red-700 text-xs text-white px-2 py-1 rounded-md">Disabled</span>
            </div>
          {/if}
          {#if item.additional_meta.includes("BETA")}
            <div>
              <span class="bg-blue-700 text-xs text-white px-2 py-1 rounded-md">Beta</span>
            </div>
          {/if}
        </div>
        <div class={`flex flex-row gap-2 items-center ${item.disabled || item.additional_meta.length > 0 ? "ml-2" : ""}`}>
          <span class={`font-semibold text-sm ${item.disabled ? 'line-through' : ''}`}>{item.name}</span>
          <code class={`font-light text-xs ${item.disabled ? 'line-through' : ''}`}>{item.type}</code>
          <span class={`text-xs ${item.disabled ? 'line-through' : item.required ? 'text-red-500' : 'text-gray-500'}`}>
            {item.required ? "Required" : "Optional"}
          </span>
          {#if item.default}
            <code class={`text-gray-500 text-xs ml-2 ${item.disabled ? 'line-through' : ''}`}>
              Default: <span class="text-gray-500 text-xs">{item.default}</span>
            </code>
          {/if}
        </div>
      </div>
      {#if !item.disabled}
        <span class="text-gray-500 text-sm">
          <SvelteMarkdown source={convertNewlinesToBr(item.description)} isInline />
        </span>
      {/if}
      {#if item.values}
        <AvailableValues values={item.values} />
      {/if}
    </div>
  {/each}
</div>

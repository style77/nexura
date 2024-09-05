<script lang="ts">
    export let values: any;

    let expanded = false;

    function toggle() {
        expanded = !expanded;
    }

    function formatValueName(valueName: string) {
        if (valueName.startsWith("_")) {
            return valueName.slice(1);
        }

        return valueName;
    }
</script>

<button
    class="mt-1 text-xs font-regular self-start my-2"
    on:click={() => toggle()}>Show available values</button
>
{#if expanded}
    <div class="flex flex-col ml-2 gap-1">
        {#if Array.isArray(values)}
            {#each values as value}
                <div class="flex flex-col ml-2">
                    <div>
                        <div class="flex flex-col">
                            <div class="flex flex-row gap-2 items-center">
                                <span class="font-semibold text-sm"
                                    >{value.name}</span
                                >
                                <code class="font-light text-xs"
                                    >{value.type}</code
                                >
                                <span class="text-xs text-gray-500"
                                    >{value.required
                                        ? "Required"
                                        : "Optional"}</span
                                >
                                {#if value.default}
                                    <code class="text-gray-500 text-xs ml-2"
                                        >Default: <span
                                            class="text-gray-500 text-xs"
                                            >{value.default}</span
                                        ></code
                                    >
                                {/if}
                            </div>
                            <span class="text-gray-500 text-sm"
                                >{value.description}</span
                            >
                        </div>
                        {#if value.values}
                            <svelte:self values={value.values} />
                        {/if}
                    </div>
                </div>
            {/each}
        {:else if typeof values === "object"}
            {#each Object.entries(values) as [valueName, value]}
                <div class="flex flex-col gap-1">
                    <div class="flex flex-row items-center">
                        <div class="flex flex-row gap-2 items-center">
                            <span class="font-semibold text-sm"
                                >{formatValueName(valueName)}</span
                            >
                        </div>
                    </div>
                    {#each value as nestedValue}
                        <div class="flex flex-col gap-4 ml-2">
                            <div>
                                <div class="flex flex-col">
                                    <div
                                        class="flex flex-row gap-2 items-center"
                                    >
                                        <span class="font-semibold text-sm"
                                            >{nestedValue.name}</span
                                        >
                                        <code class="font-light text-xs"
                                            >{nestedValue.type}</code
                                        >
                                        <span class="text-xs text-gray-500"
                                            >{nestedValue.required
                                                ? "Required"
                                                : "Optional"}</span
                                        >
                                        {#if nestedValue.default}
                                            <code
                                                class="text-gray-500 text-xs ml-2"
                                                >Default: <span
                                                    class="text-gray-500 text-xs"
                                                    >{nestedValue.default}</span
                                                ></code
                                            >
                                        {/if}
                                    </div>
                                    <span class="text-gray-500 text-sm"
                                        >{nestedValue.description}</span
                                    >
                                </div>
                                {#if nestedValue.values}
                                    <svelte:self values={nestedValue.values} />
                                {/if}
                            </div>
                        </div>
                    {/each}
                </div>
            {/each}
        {/if}
    </div>
{/if}

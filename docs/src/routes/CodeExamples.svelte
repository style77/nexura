<script lang="ts">
    import { writable, derived } from "svelte/store";
    import { CodeBlock } from "svhighlight";
    import "highlight.js/styles/base16/dracula.css";

    export let examples: {
        label: string;
        code: Record<string, string | undefined>;
        response: {
            type: string;
            content: string;
        };
    }[];

    const selectedExample = writable(examples[0]);
    const selectedLanguage = writable(Object.keys(examples[0].code)[0]);

    $: availableLanguages = Object.keys($selectedExample.code);

    $: if (!availableLanguages.includes($selectedLanguage)) {
        selectedLanguage.set(availableLanguages[0]);
    }

    const currentCode = derived(
        [selectedExample, selectedLanguage],
        ([$selectedExample, $selectedLanguage]) =>
            $selectedExample.code[$selectedLanguage],
    );

    // Debugging
    $: console.log("Selected Example:", $selectedExample);
    $: console.log("Selected Language:", $selectedLanguage);
    $: console.log("Current Code:", $currentCode);
</script>

<div class="bg-gray-900 text-white p-4 rounded-lg overflow-auto w-full">
    <div class="flex space-x-2 mb-4">
        {#each examples as example}
            <button
                class="px-3 py-1 rounded {$selectedExample === example
                    ? 'bg-gray-700'
                    : 'bg-gray-800 hover:bg-gray-700'}"
                on:click={() => selectedExample.set(example)}
            >
                {example.label}
            </button>
        {/each}
    </div>

    <div class="mb-4">
        <label for="language-select" class="block text-sm font-medium mb-2"
            >Select Language:</label
        >
        <select
            id="language-select"
            bind:value={$selectedLanguage}
            class="bg-gray-800 text-white rounded px-3 py-1"
        >
            {#each availableLanguages as language}
                <option value={language}>{language}</option>
            {/each}
        </select>
    </div>

    <div class="flex flex-col gap-4">
        <div>
            <span class="font-semibold text-xl mb-2 block">Request</span>
            {#key $selectedLanguage}
                <CodeBlock
                    language={$selectedLanguage}
                    code={$currentCode}
                />
            {/key}
        </div>

        <div>
            <span class="font-semibold text-xl mb-2 block">Response</span>
            {#key $selectedExample}
                <CodeBlock
                    language={$selectedExample.response.type}
                    code={$selectedExample.response.content}
                />
            {/key}
        </div>
    </div>
</div>

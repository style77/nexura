<script lang="ts">
  import RequestType from "./RequestType.svelte";
  import { selectedProvider, selectedEndpoint } from "$lib/store";
  import { onDestroy } from "svelte";
  import docsJson from "../docs.json";
  import type { Docs } from "$lib/types";
  import CodeExamples from "./CodeExamples.svelte";

  const docs: Docs = docsJson;

  let selectedProviderValue: string = "";
  let selectedEndpointValue: string = "";
  const endpointRefs: Record<string, HTMLElement | null> = {};

  const getMethodColor = (method: string) => {
    switch (method) {
      case "GET":
        return "bg-green-200 text-green-500";
      case "POST":
        return "bg-blue-200 text-blue-500";
      case "PUT":
        return "bg-yellow-200 text-yellow-500";
      case "DELETE":
        return "bg-red-200 text-red-500";
      default:
        return "bg-gray-200 text-gray-500";
    }
  };

  const copyEndpointUrl = (endpointUrl: string) => {
    const copyButton = document.getElementById(`copy-${endpointUrl}`);
    copyButton?.classList.add("bg-blue-300/50");
    setTimeout(() => {
      copyButton?.classList.remove("bg-blue-300/50");
    }, 300);

    const el = document.createElement("textarea");
    const formattedEndpointUrl = endpointUrl.replace(/ /g, "-").toLowerCase();
    el.value = `${window.location.origin}/${selectedProviderValue}/${formattedEndpointUrl}`;
    document.body.appendChild(el);
    el.select();
    document.execCommand("copy");
    document.body.removeChild(el);
  };

  const unsubscribeProvider = selectedProvider.subscribe((value) => {
    selectedProviderValue = value;
  });

  const unsubscribeEndpoint = selectedEndpoint.subscribe((value) => {
    selectedEndpointValue = value;
    if (endpointRefs[selectedEndpointValue]) {
      endpointRefs[selectedEndpointValue]?.scrollIntoView({
        behavior: "smooth",
      });
    }
  });

  onDestroy(() => {
    unsubscribeProvider();
    unsubscribeEndpoint();
  });
</script>

<svelte:head>
  <title>Nexura Documentation</title>
  <meta name="description" content="Nexura documentation" />
</svelte:head>

<main class="p-6">
  {#if !selectedProviderValue}
    <p class="text-xl font-semibold">Select a provider to view its endpoints</p>
  {/if}
  {#if selectedProviderValue && !docs[selectedProviderValue]}
    <p class="text-xl font-semibold">
      No documentation found for selected provider
    </p>
  {/if}

  {#if selectedProviderValue && docs[selectedProviderValue] && docs[selectedProviderValue].endpoints}
    <div class="mt-6">
      {#each Object.entries(docs[selectedProviderValue].endpoints || {}) as [providerName, provider]}
        <div class="mb-3">
          <p class="text-xl font-semibold">
            {docs[selectedProviderValue].name}
          </p>
          <p class="text-gray-500 text-sm">
            {docs[selectedProviderValue].description}
          </p>
        </div>
        <div>
          {#each Object.entries(docs[selectedProviderValue].endpoints) as [endpointName, endpoint]}
            <div class="flex flex-row gap-4 justify-between">
              <div class="flex flex-col gap-4">
                <div>
                  <div class="flex flex-col">
                    <div class="flex flex-row gap-2 items-center">
                      <button
                        on:click={() => copyEndpointUrl(endpoint.name)}
                        class="flex flex-row gap-2 items-center transition my-1 duration-300 ease-in-out rounded cursor-pointer px-2 py-0.5"
                        id={`copy-${endpoint.name}`}
                      >
                        <svg
                          xmlns="http://www.w3.org/2000/svg"
                          width="18px"
                          height="18px"
                          fill="currentColor"
                          viewBox="0 0 24 24"
                          class="animate-in"
                          ><path
                            fill-rule="evenodd"
                            d="M7 5a3 3 0 0 1 3-3h9a3 3 0 0 1 3 3v9a3 3 0 0 1-3 3h-2v2a3 3 0 0 1-3 3H5a3 3 0 0 1-3-3v-9a3 3 0 0 1 3-3h2V5Zm2 2h5a3 3 0 0 1 3 3v5h2a1 1 0 0 0 1-1V5a1 1 0 0 0-1-1h-9a1 1 0 0 0-1 1v2ZM5 9a1 1 0 0 0-1 1v9a1 1 0 0 0 1 1h9a1 1 0 0 0 1-1v-9a1 1 0 0 0-1-1H5Z"
                            clip-rule="evenodd"
                          ></path></svg
                        >
                        <p
                          class="text-lg font-semibold"
                          bind:this={endpointRefs[endpoint.name]}
                          id={endpoint.name}
                        >
                          {endpoint.name}
                        </p>
                      </button>
                      <div
                        class="bg-gray-200 text-gray-500 text-sm px-2 py-1 rounded"
                      >
                        {endpoint.category}
                      </div>
                    </div>
                    <div class="flex flex-row gap-2 items-center">
                      <div
                        class={`${getMethodColor(endpoint.method)} text-xs px-1.5 py-1 rounded`}
                      >
                        {endpoint.method}
                      </div>
                      <code class="text-gray-500 text-xs">
                        {endpoint.nexuraPath}
                      </code>
                    </div>
                  </div>
                  <p class="text-gray-500 text-sm mt-2">
                    {endpoint.description}
                  </p>
                </div>
                <div>
                  <p class="font-semibold text-lg">Request Type</p>
                  <RequestType data={endpoint.request_type} />
                </div>
                <div>
                  <p class="font-semibold text-lg">Response Type</p>
                  <RequestType data={endpoint.return_type} />
                </div>
              </div>
              <div class="lg:flex flex-col hidden min-w-[500px]">
                {#if endpoint.examples && endpoint.examples.length > 0}
                  <CodeExamples examples={endpoint.examples} />
                {/if}
              </div>
            </div>
          {/each}
        </div>
      {/each}
    </div>
  {/if}
</main>

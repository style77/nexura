<script lang="ts">
  import RequestType from "./RequestType.svelte";
  import { selectedProvider, selectedEndpoint } from "$lib/store";
  import { onDestroy, onMount } from "svelte";
  import docs from "../docs.json";
  import CodeExamples from "./CodeExamples.svelte";

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

  const examples = [
    {
      label: "Example 1",
      code: {
        python: `from openai import OpenAI
client = OpenAI()

tools = [
    {
        "type": "function",
        "function": {
            "name": "get_current_weather",
            "description": "Get the current weather in a given location",
            "parameters": {
                "type": "object",
                "properties": {
                    "location": {
                        "type": "string",
                        "description": "The city and state, e.g. San Francisco, CA"
                    },
                    "unit": {"type": "string", "enum": ["celsius", "fahrenheit"]}
                },
                "required": ["location"]
            }
        }
    }
]

response = client.chat.completions.create(
    model="gpt-3.5-turbo-0613",
    messages=[{"role": "user", "content": "What's the weather like in Boston?"}],
    tools=tools,
    tool_choice="auto",
)`,
        javascript: `import OpenAI from 'openai';

const client = new OpenAI();

const tools = [
    {
        "type": "function",
        "function": {
            "name": "get_current_weather",
            "description": "Get the current weather in a given location",
            "parameters": {
                "type": "object",
                "properties": {
                    "location": {
                        "type": "string",
                        "description": "The city and state, e.g. San Francisco, CA"
                    },
                    "unit": {"type": "string", "enum": ["celsius", "fahrenheit"]}
                },
                "required": ["location"]
            }
        }
    }
];

const response = await client.chat.completions.create({
    model: "gpt-3.5-turbo-0613",
    messages: [{"role": "user", "content": "What's the weather like in Boston?"}],
    tools: tools,
    tool_choice: "auto",
});`,
      },
      response: {
        type: "json",
        content: `{
    "id": "chatcmpl-123",
    "object": "chat.completion",
    "created": 1677652288,
    "model": "gpt-3.5-turbo-0613",
    "choices": [{
        "index": 0,
        "message": {
            "role": "assistant",
            "content": null,
            "tool_calls": [
                {
                    "id": "call_abc123",
                    "type": "function",
                    "function": {
                        "name": "get_current_weather",
                        "arguments": "{\n  \"location\": \"Boston, MA\"\n}"
                    }
                }
            ]
        },
        "finish_reason": "tool_calls"
    }],
    "usage": {
        "prompt_tokens": 82,
        "completion_tokens": 37,
        "total_tokens": 119
    }
}`,
      },
    },
    // Add more examples here
  ];
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
                {#if endpoint.examples.length > 0}
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

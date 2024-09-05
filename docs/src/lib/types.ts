interface RequestType {
    name: string;
    type: string;
    genericType: string;
    description: string;
    default: any;
    required: boolean;
    disabled: boolean | string;
    hidden: boolean;
    additional_meta: any[];
    values: any[] | null | Record<string, any>;
}

interface Example {
    label: string;
    code: Record<string, string | undefined>;
    response: {
        type: string;
        content: string;
    };
}

interface Endpoint {
    name: string;
    method: string;
    path: string;
    nexuraPath: string;
    category: string;
    description: string;
    original_docs_url: string;
    request_type: RequestType[];
    return_type: RequestType[];
    examples?: Example[] | [];
}

interface Provider {
    name: string;
    description: string;
    endpoints: Record<string, Endpoint>;
}

export interface Docs {
    [provider: string]: Provider;
}
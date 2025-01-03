

export type StorageClient = {
  downloadFile: (key: string) => Promise<string>;
  uploadFile: (key: string, base64: string) => Promise<void>;
}
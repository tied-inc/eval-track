import { type StorageClient } from "./base";

const downloadFile = async (key: string) => {
  throw new Error("Not implemented");
}

const uploadFile = async (key: string, base64: string) => {
  throw new Error("Not implemented");
};


export const inMemoryClient = (): StorageClient => {
  return {
    uploadFile,
    downloadFile
  }
}
import { StorageClient } from "@/utils/storage/base";
import { s3Client } from "@/utils/storage/s3";
import { inMemoryClient } from "@/utils/storage/in-memory";

export type StorageType = "s3" | "in-memory";

export const getStorageClient = (storageType: StorageType): StorageClient => {
  switch (storageType){
    case "s3":
      return s3Client();
    case "in-memory":
      return inMemoryClient();
    default:
      throw new Error("Invalid storage type");
  }
}
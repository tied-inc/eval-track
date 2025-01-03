import { PutObjectCommand, S3Client } from "@aws-sdk/client-s3";
import { awsSettings } from "@/const";
import {type StorageClient} from "./base";

const getClient = () => {
  return new S3Client({region: awsSettings.region});
}

const downloadFile = async (key: string) => {
  throw new Error("Not implemented");
}

const uploadFile = async (key: string, base64: string) => {
  try {
    const client = getClient();
    const command = new PutObjectCommand({
      Bucket: awsSettings.bucketName,
      Key: key,
      Body: Buffer.from(base64.split(",")[1], "base64"),
    });

    await client
      .send(command)
      .then(() => {
        console.log("File uploaded successfully");
      })
      .catch((error) => {
        console.error("Error uploading file:", error);
        throw error;
      });
    return;

  } catch (error) {
    console.error("Error uploading file:", error);
    throw error;
  }
};


export const s3Client = (): StorageClient => {
  return {
    uploadFile,
    downloadFile
  }
}
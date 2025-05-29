/**
 * AWS Resources API service
 * Handles all API calls related to AWS resources
 */

import { get } from './api';

// Types
export interface EC2Instance {
  id: string;
  name: string;
  type: string;
  state: string;
  region: string;
}

export interface S3Bucket {
  name: string;
  creation_date: string;
  region: string;
}

export interface RDSInstance {
  id: string;
  engine: string;
  status: string;
  storage: number;
  region: string;
}

export interface AWSResources {
  ec2_instances: EC2Instance[];
  s3_buckets: S3Bucket[];
  rds_instances: RDSInstance[];
}

// API endpoints
const AWS_RESOURCES_ENDPOINT = '/aws-resources';

/**
 * Get all AWS resources for an account
 */
export const getAWSResources = async (accountId: string): Promise<AWSResources> => {
  return get(`${AWS_RESOURCES_ENDPOINT}/${accountId}`);
};

/**
 * Get EC2 instances for an AWS account
 */
export const getEC2Instances = async (accountId: string): Promise<EC2Instance[]> => {
  return get(`${AWS_RESOURCES_ENDPOINT}/${accountId}/ec2`);
};

/**
 * Get S3 buckets for an AWS account
 */
export const getS3Buckets = async (accountId: string): Promise<S3Bucket[]> => {
  return get(`${AWS_RESOURCES_ENDPOINT}/${accountId}/s3`);
};

/**
 * Get RDS instances for an AWS account
 */
export const getRDSInstances = async (accountId: string): Promise<RDSInstance[]> => {
  return get(`${AWS_RESOURCES_ENDPOINT}/${accountId}/rds`);
};

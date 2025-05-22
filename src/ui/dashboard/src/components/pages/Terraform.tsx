import React, { useState, useEffect } from 'react';
import { Card, CardContent, CardDescription, CardFooter, CardHeader, CardTitle } from "@/components/ui/card";
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import { Textarea } from "@/components/ui/textarea";
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "@/components/ui/select";
import { Table, TableBody, TableCaption, TableCell, TableHead, TableHeader, TableRow } from "@/components/ui/table";
import { Badge } from "@/components/ui/badge";
import { Separator } from "@/components/ui/separator";
import { ScrollArea } from "@/components/ui/scroll-area";
import { AlertCircle, CheckCircle, Clock, Code, FileText, Play, Plus, RefreshCw, Trash2 } from "lucide-react";
import { 
  getTerraformTemplates, 
  getTerraformDeployments, 
  createTerraformTemplate, 
  deleteTerraformTemplate, 
  deployTerraformTemplate 
} from '@/lib/api';
import { TerraformTemplate, TerraformDeployment } from '@/lib/types';

const Terraform: React.FC = () => {
  const [activeTab, setActiveTab] = useState('templates');
  const [templates, setTemplates] = useState<TerraformTemplate[]>([]);
  const [deployments, setDeployments] = useState<TerraformDeployment[]>([]);
  const [loading, setLoading] = useState(false);
  const [newTemplate, setNewTemplate] = useState({
    name: '',
    description: '',
    variables: '',
    content: '',
    provider: 'aws'
  });
  const [selectedTemplate, setSelectedTemplate] = useState<TerraformTemplate | null>(null);
  const [deploymentVars, setDeploymentVars] = useState<Record<string, string>>({});
  const [deploymentName, setDeploymentName] = useState('');
  const [deploymentStatus, setDeploymentStatus] = useState('');

  useEffect(() => {
    fetchTemplates();
    fetchDeployments();
  }, []);

  const fetchTemplates = async () => {
    setLoading(true);
    try {
      const response = await getTerraformTemplates();
      if (response.success && response.data) {
        setTemplates(response.data);
      }
    } catch (error) {
      console.error('Error fetching templates:', error);
    } finally {
      setLoading(false);
    }
  };

  const fetchDeployments = async () => {
    setLoading(true);
    try {
      const response = await getTerraformDeployments();
      if (response.success && response.data) {
        setDeployments(response.data);
      }
    } catch (error) {
      console.error('Error fetching deployments:', error);
    } finally {
      setLoading(false);
    }
  };

  const handleCreateTemplate = async () => {
    setLoading(true);
    try {
      await createTerraformTemplate(newTemplate);
      setNewTemplate({
        name: '',
        description: '',
        variables: '',
        content: '',
        provider: 'aws'
      });
      fetchTemplates();
    } catch (error) {
      console.error('Error creating template:', error);
    } finally {
      setLoading(false);
    }
  };

  const handleDeleteTemplate = async (id: string) => {
    if (confirm('Are you sure you want to delete this template?')) {
      setLoading(true);
      try {
        await deleteTerraformTemplate(id);
        fetchTemplates();
      } catch (error) {
        console.error('Error deleting template:', error);
      } finally {
        setLoading(false);
      }
    }
  };

  const handleSelectTemplate = (template: TerraformTemplate) => {
    setSelectedTemplate(template);
    // Parse variables and initialize deploymentVars
    try {
      const vars = JSON.parse(template.variables);
      const initialVars: Record<string, string> = {};
      Object.keys(vars).forEach(key => {
        initialVars[key] = vars[key].default || '';
      });
      setDeploymentVars(initialVars);
    } catch (error) {
      console.error('Error parsing variables:', error);
      setDeploymentVars({});
    }
  };

  const handleDeployTemplate = async () => {
    if (!selectedTemplate) return;
    
    setLoading(true);
    setDeploymentStatus('deploying');
    
    try {
      await deployTerraformTemplate(
        selectedTemplate.id,
        deploymentVars
      );
      setDeploymentStatus('success');
      fetchDeployments();
      setActiveTab('deployments');
    } catch (error) {
      console.error('Error deploying template:', error);
      setDeploymentStatus('error');
    } finally {
      setLoading(false);
    }
  };

  const handleDestroyDeployment = async (id: string) => {
    if (confirm('Are you sure you want to destroy this deployment? This action cannot be undone.')) {
      setLoading(true);
      try {
        // Since this function doesn't exist in the API, we'll just log it for now
        console.log('Would destroy deployment:', id);
        // In a real implementation, you would call the API:
        // await destroyTerraformDeployment(id);
        fetchDeployments();
      } catch (error) {
        console.error('Error destroying deployment:', error);
      } finally {
        setLoading(false);
      }
    }
  };

  const renderTemplatesList = () => (
    <div className="space-y-4">
      <div className="flex justify-between items-center">
        <h3 className="text-lg font-medium">Available Templates</h3>
        <Button onClick={fetchTemplates} variant="outline" size="sm">
          <RefreshCw className="h-4 w-4 mr-2" />
          Refresh
        </Button>
      </div>
      
      {templates.length === 0 ? (
        <Card>
          <CardContent className="pt-6">
            <p className="text-center text-muted-foreground">No templates available. Create your first template.</p>
          </CardContent>
        </Card>
      ) : (
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
          {templates.map(template => (
            <Card key={template.id} className="hover:shadow-md transition-shadow">
              <CardHeader className="pb-2">
                <div className="flex justify-between items-start">
                  <CardTitle className="text-base">{template.name}</CardTitle>
                  <Badge variant="outline">{template.provider}</Badge>
                </div>
                <CardDescription className="line-clamp-2">{template.description}</CardDescription>
              </CardHeader>
              <CardFooter className="flex justify-between pt-2">
                <Button variant="outline" size="sm" onClick={() => handleSelectTemplate(template)}>
                  Select
                </Button>
                <Button variant="ghost" size="sm" onClick={() => handleDeleteTemplate(template.id)}>
                  <Trash2 className="h-4 w-4 text-destructive" />
                </Button>
              </CardFooter>
            </Card>
          ))}
        </div>
      )}
    </div>
  );

  const renderNewTemplateForm = () => (
    <Card>
      <CardHeader>
        <CardTitle>Create New Template</CardTitle>
        <CardDescription>Define a new Terraform template for infrastructure provisioning</CardDescription>
      </CardHeader>
      <CardContent className="space-y-4">
        <div className="grid grid-cols-2 gap-4">
          <div className="space-y-2">
            <Label htmlFor="template-name">Template Name</Label>
            <Input 
              id="template-name" 
              value={newTemplate.name} 
              onChange={e => setNewTemplate({...newTemplate, name: e.target.value})}
              placeholder="e.g., AWS S3 Bucket"
            />
          </div>
          <div className="space-y-2">
            <Label htmlFor="template-provider">Cloud Provider</Label>
            <Select 
              value={newTemplate.provider} 
              onValueChange={value => setNewTemplate({...newTemplate, provider: value})}
            >
              <SelectTrigger>
                <SelectValue placeholder="Select provider" />
              </SelectTrigger>
              <SelectContent>
                <SelectItem value="aws">AWS</SelectItem>
                <SelectItem value="azure">Azure</SelectItem>
                <SelectItem value="gcp">Google Cloud</SelectItem>
              </SelectContent>
            </Select>
          </div>
        </div>
        
        <div className="space-y-2">
          <Label htmlFor="template-description">Description</Label>
          <Textarea 
            id="template-description" 
            value={newTemplate.description} 
            onChange={e => setNewTemplate({...newTemplate, description: e.target.value})}
            placeholder="Describe what this template provisions"
            rows={2}
          />
        </div>
        
        <div className="space-y-2">
          <Label htmlFor="template-variables">
            Variables (JSON format)
            <span className="text-xs text-muted-foreground ml-2">Define variables with type, description, and default values</span>
          </Label>
          <Textarea 
            id="template-variables" 
            value={newTemplate.variables} 
            onChange={e => setNewTemplate({...newTemplate, variables: e.target.value})}
            placeholder={`{
  "bucket_name": {
    "type": "string",
    "description": "Name of the S3 bucket",
    "default": "my-terraform-bucket"
  }
}`}
            rows={6}
            className="font-mono text-sm"
          />
        </div>
        
        <div className="space-y-2">
          <Label htmlFor="template-content">
            Terraform Configuration
            <span className="text-xs text-muted-foreground ml-2">HCL format</span>
          </Label>
          <Textarea 
            id="template-content" 
            value={newTemplate.content} 
            onChange={e => setNewTemplate({...newTemplate, content: e.target.value})}
            placeholder={`provider "aws" {
  region = "us-east-1"
}

resource "aws_s3_bucket" "example" {
  bucket = var.bucket_name
  acl    = "private"
  
  tags = {
    Name        = var.bucket_name
    Environment = "Dev"
  }
}`}
            rows={12}
            className="font-mono text-sm"
          />
        </div>
      </CardContent>
      <CardFooter>
        <Button onClick={handleCreateTemplate} disabled={loading}>
          {loading ? 'Creating...' : 'Create Template'}
        </Button>
      </CardFooter>
    </Card>
  );

  const renderDeploymentForm = () => {
    if (!selectedTemplate) {
      return (
        <Card>
          <CardContent className="pt-6 pb-6">
            <p className="text-center text-muted-foreground">Select a template from the list to deploy</p>
          </CardContent>
        </Card>
      );
    }

    return (
      <Card>
        <CardHeader>
          <CardTitle>Deploy Template: {selectedTemplate.name}</CardTitle>
          <CardDescription>{selectedTemplate.description}</CardDescription>
        </CardHeader>
        <CardContent className="space-y-4">
          <div className="space-y-2">
            <Label htmlFor="deployment-name">Deployment Name</Label>
            <Input 
              id="deployment-name" 
              value={deploymentName} 
              onChange={e => setDeploymentName(e.target.value)}
              placeholder="e.g., production-s3-bucket"
            />
          </div>
          
          <Separator />
          
          <div className="space-y-4">
            <h4 className="text-sm font-medium">Configuration Variables</h4>
            
            {Object.keys(deploymentVars).length === 0 ? (
              <p className="text-sm text-muted-foreground">No variables defined for this template</p>
            ) : (
              Object.keys(deploymentVars).map(key => {
                let description = '';
                try {
                  const vars = JSON.parse(selectedTemplate.variables);
                  description = vars[key]?.description || '';
                } catch (e) {}
                
                return (
                  <div key={key} className="space-y-2">
                    <Label htmlFor={`var-${key}`}>
                      {key}
                      {description && <span className="text-xs text-muted-foreground ml-2">{description}</span>}
                    </Label>
                    <Input 
                      id={`var-${key}`} 
                      value={deploymentVars[key]} 
                      onChange={e => setDeploymentVars({...deploymentVars, [key]: e.target.value})}
                    />
                  </div>
                );
              })
            )}
          </div>
        </CardContent>
        <CardFooter className="flex justify-between">
          <Button variant="outline" onClick={() => setSelectedTemplate(null)}>
            Cancel
          </Button>
          <Button onClick={handleDeployTemplate} disabled={loading || !deploymentName}>
            {loading ? 'Deploying...' : 'Deploy Infrastructure'}
          </Button>
        </CardFooter>
      </Card>
    );
  };

  const renderDeploymentsList = () => (
    <div className="space-y-4">
      <div className="flex justify-between items-center">
        <h3 className="text-lg font-medium">Active Deployments</h3>
        <Button onClick={fetchDeployments} variant="outline" size="sm">
          <RefreshCw className="h-4 w-4 mr-2" />
          Refresh
        </Button>
      </div>
      
      {deployments.length === 0 ? (
        <Card>
          <CardContent className="pt-6">
            <p className="text-center text-muted-foreground">No active deployments. Deploy a template to get started.</p>
          </CardContent>
        </Card>
      ) : (
        <div className="rounded-md border">
          <Table>
            <TableHeader>
              <TableRow>
                <TableHead>Name</TableHead>
                <TableHead>Template</TableHead>
                <TableHead>Status</TableHead>
                <TableHead>Created</TableHead>
                <TableHead className="text-right">Actions</TableHead>
              </TableRow>
            </TableHeader>
            <TableBody>
              {deployments.map(deployment => (
                <TableRow key={deployment.id}>
                  <TableCell className="font-medium">{deployment.name}</TableCell>
                  <TableCell>{deployment.templateName}</TableCell>
                  <TableCell>
                    {deployment.status === 'active' && (
                      <Badge variant="outline" className="bg-green-100 text-green-800">
                        <CheckCircle className="h-3 w-3 mr-1" /> Active
                      </Badge>
                    )}
                    {deployment.status === 'deploying' && (
                      <Badge variant="outline" className="bg-blue-100 text-blue-800">
                        <Clock className="h-3 w-3 mr-1" /> Deploying
                      </Badge>
                    )}
                    {deployment.status === 'failed' && (
                      <Badge variant="destructive">
                        <AlertCircle className="h-3 w-3 mr-1" /> Failed
                      </Badge>
                    )}
                  </TableCell>
                  <TableCell>{new Date(deployment.createdAt).toLocaleDateString()}</TableCell>
                  <TableCell className="text-right">
                    <Button variant="ghost" size="sm" className="h-8 w-8 p-0" onClick={() => handleDestroyDeployment(deployment.id)}>
                      <Trash2 className="h-4 w-4 text-destructive" />
                    </Button>
                  </TableCell>
                </TableRow>
              ))}
            </TableBody>
          </Table>
        </div>
      )}
    </div>
  );

  return (
    <div className="container mx-auto py-6 space-y-8">
      <div>
        <h2 className="text-3xl font-bold tracking-tight">Terraform Management</h2>
        <p className="text-muted-foreground">
          Create, deploy, and manage infrastructure as code across cloud providers
        </p>
      </div>
      
      <Tabs value={activeTab} onValueChange={setActiveTab} className="space-y-4">
        <TabsList>
          <TabsTrigger value="templates">
            <FileText className="h-4 w-4 mr-2" />
            Templates
          </TabsTrigger>
          <TabsTrigger value="deployments">
            <Code className="h-4 w-4 mr-2" />
            Deployments
          </TabsTrigger>
        </TabsList>
        
        <TabsContent value="templates" className="space-y-6">
          <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
            <div className="space-y-6">
              {renderTemplatesList()}
            </div>
            <div>
              {renderNewTemplateForm()}
            </div>
          </div>
        </TabsContent>
        
        <TabsContent value="deployments" className="space-y-6">
          <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
            <div className="space-y-6">
              {renderDeploymentsList()}
            </div>
            <div>
              {renderDeploymentForm()}
            </div>
          </div>
        </TabsContent>
      </Tabs>
    </div>
  );
};

export default Terraform;

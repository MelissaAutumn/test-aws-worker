# AWS Worker for automated environment deployment

## Commands

Deploy all stacks with:
`cdk deploy --require-approval never --outputs-file cdk.out.json`
Deploy specific stack with:
`cdk deploy "StackNameHere" --require-approval never --outputs-file cdk.out.json`
Destroy all stacks with:
`cdk destroy --force`
Destroy specific stack with:
`cdk destroy "StackNameHere" --force`

You can append `--verbose` if it's a little too quiet for you.

Note: Currently it's setup to build the stack name from environment variables, so if those variables aren't consistent I'm not sure if it will destroy all stacks properly. You can always visit CloudFormation's Stacks page to manually nuke things.

## Stacks
 - PreviewStack : Deploys a docker image from a freshly built `thunderbird.net/` directory on `thunderbird-website` repo.

## Environment Variables

### Preview Stack
 - `PS_PREVIEW_ENV_ID` : Unique ID for pull request preview environment deploys. Should be formatted like `{Branch Name}-{PR Number}`. Defaults to `fake-branch-name-400`.
 - `PS_SITE_NAME` : Unique site id. All assets/services/vpcs/etc will be prefixed by this. Defaults to `thunderbird-website`.
 - `PS_NAMESPACE` : For the cluster's cluod map. Defaults to `thunderbird.local`.
 - `PS_DOCKER_DIRECTORY` : Directory where the docker file is. Defaults to `../thunderbird-website`. 
 - `PS_DOCKER_FILE` : Docker file name. Defaults to `deploy.docker`.

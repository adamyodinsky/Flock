
@router.delete(
        f"/deployment_resource/{kind}/{category}/{namespace}/{name}",
        description="Delete deployment",
    )

    # fetch the deployment schema from the resource store and delete it


@router.put("/deployment_resource")
  
  # validate the body with the deployment schema and then use the deployer to validate with dry run, and in the end save to the resource store

@router.put("/deployment_instance")

  # validate the body with the deployment instance schema and then use the deployer to validate with dry run, and in the end save to the resource store and run the deployment
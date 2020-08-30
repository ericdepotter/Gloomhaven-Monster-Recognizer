// Fill out your copyright notice in the Description page of Project Settings.


#include "SpawnLocation.h"

// Sets default values for this component's properties
USpawnLocation::USpawnLocation()
{
	// Set this component to be initialized when the game starts, and to be ticked every frame.  You can turn these features
	// off to improve performance if you don't need them.
	PrimaryComponentTick.bCanEverTick = false;

	StaticMeshComponent = CreateDefaultSubobject<UStaticMeshComponent>(FName("MeshComponent"));
	StaticMeshComponent->AttachToComponent(
		this,
		FAttachmentTransformRules::SnapToTargetIncludingScale
	);

	auto Result = ConstructorHelpers::FObjectFinder<UStaticMesh>(TEXT("StaticMesh'/Engine/BasicShapes/Cone.Cone'"));
	if (Result.Object)
	{
		StaticMeshComponent->SetStaticMesh(Result.Object);
		StaticMeshComponent->SetWorldScale3D(FVector(Scale, Scale, Scale));
	}
}


// Called when the game starts
void USpawnLocation::BeginPlay()
{
	Super::BeginPlay();

	StaticMeshComponent->SetStaticMesh(nullptr);
	StaticMeshComponent->UnregisterComponent();
}

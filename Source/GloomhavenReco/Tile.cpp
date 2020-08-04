// Fill out your copyright notice in the Description page of Project Settings.

#include "SpawnLocation.h"
#include "Tile.h"
#include "Math/UnrealMathUtility.h"

// Sets default values
ATile::ATile()
{
 	// Set this actor to call Tick() every frame.  You can turn this off to improve performance if you don't need it.
	PrimaryActorTick.bCanEverTick = false;

	USceneComponent* Root = CreateDefaultSubobject<USceneComponent>(FName("RootSceneComponent"));
	Root->AttachToComponent(
		nullptr,
		FAttachmentTransformRules::SnapToTargetNotIncludingScale
	);

	SetRootComponent(Root);

	StaticMeshComponent = CreateDefaultSubobject<UStaticMeshComponent>(FName("MeshComponent"));
	StaticMeshComponent->AttachToComponent(
		Root,
		FAttachmentTransformRules::SnapToTargetIncludingScale
	);

	auto Result = ConstructorHelpers::FObjectFinder<UStaticMesh>(TEXT("StaticMesh'/Engine/BasicShapes/Cube.Cube'"));
	if (Result.Object)
	{
		StaticMeshComponent->SetStaticMesh(Result.Object);
	}
}

// Called when the game starts or when spawned
void ATile::BeginPlay()
{
	Super::BeginPlay();
}

TArray<USpawnLocation*> ATile::GetSpawnLocations() const
{
	TArray<USpawnLocation*> OutComponents;
	GetComponents<USpawnLocation>(OutComponents);
	return OutComponents;
}

void ATile::PopulateTile(FVector CameraPosition, int NumberMonsters) 
{
	TArray<USpawnLocation*> SpawnLocations = GetSpawnLocations();
	NumberMonsters = FMath::Clamp(NumberMonsters, 1, SpawnLocations.Num());

	for (int i = 0; i < NumberMonsters; i++)
	{
		int index = FMath::RandRange(0, SpawnLocations.Num() - 1);

		USpawnLocation* SpawnLocation = SpawnLocations[index];
		SpawnLocations.RemoveAt(index);

		UE_LOG(LogTemp, Warning, TEXT("Monster at %s"), *SpawnLocation->GetComponentLocation().ToString());
	}
}

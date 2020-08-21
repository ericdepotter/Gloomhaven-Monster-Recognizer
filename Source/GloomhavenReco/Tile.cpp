// Fill out your copyright notice in the Description page of Project Settings.

#include "SpawnLocation.h"
#include "Monster.h"
#include "Tile.h"
#include "Kismet/KismetMathLibrary.h"
#include "Math/UnrealMathUtility.h"
#include "Engine.h"

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
	if (Monsters.Num() > 0)
	{
		ClearTile();
	}

	TArray<USpawnLocation*> SpawnLocations = GetSpawnLocations();
	NumberMonsters = FMath::Clamp(NumberMonsters, 1, SpawnLocations.Num());

	for (int i = 0; i < NumberMonsters; i++)
	{
		int index = FMath::RandRange(0, SpawnLocations.Num() - 1);

		USpawnLocation* SpawnLocation = SpawnLocations[index];
		SpawnLocations.RemoveAt(index);

		FVector Location = SpawnLocation->GetComponentLocation() + FVector(0, 0, -20);
		FRotator LookAtCameraRotation = UKismetMathLibrary::FindLookAtRotation(Location, CameraPosition);
		float Yaw = LookAtCameraRotation.Yaw - 90 + 180 * FMath::RandRange(0, 1) + FMath::RandRange(-30.f, 30.f);
		SpawnMonster(Location, FRotator(0, Yaw, 0));
	}
}

void ATile::SwitchToMask() 
{
	if (MaskMaterial)
	{
		StaticMeshComponent->SetMaterial(0, MaskMaterial);
	}
	else 
	{
		UE_LOG(LogTemp, Error, TEXT("Tile '%s' does not have a mask material"), *GetName());
	}

	for (AMonster* Monster: Monsters)
	{
		Monster->SwitchToMask();
	}
}

void ATile::ClearTile()
{
	StaticMeshComponent->SetMaterial(0, TileMaterial);
	
	for (AMonster* Monster: Monsters)
	{
		Monster->Destroy();
	}
	Monsters.Empty();
}

TArray<FString> ATile::GetBoundingBoxDescriptionsOfMonsters() const
{
	TArray<FString> result;
	//result.Add("Monster,Center_X,Center_Y,Width,Height");

	for (AMonster* Monster: Monsters)
	{
		TArray<FString> MonsterDescription;
		FBox2D BoundingBox = Monster->GetScreenBoundingBox();
		FVector2D Center = BoundingBox.GetCenter();
		FVector2D Size = BoundingBox.GetSize();

		FVector2D ScreenSize = FVector2D(1, 1);
		if (GEngine && GEngine->GameViewport)
		{
			GEngine->GameViewport->GetViewportSize(ScreenSize);
		}

		MonsterDescription.Add(Monster->GetMonsterName());
		MonsterDescription.Add(FString::SanitizeFloat((ScreenSize.X - Center.X) / ScreenSize.X));
		MonsterDescription.Add(FString::SanitizeFloat((ScreenSize.Y - Center.Y) / ScreenSize.Y));
		MonsterDescription.Add(FString::SanitizeFloat(Size.X / ScreenSize.X));
		MonsterDescription.Add(FString::SanitizeFloat(Size.Y / ScreenSize.Y));

		result.Add(FString::Join(MonsterDescription, TEXT(",")));
	}

	return result;
}

int ATile::GetNumberSpawnPoints() const
{
	return NumberSpawnPoints;
}
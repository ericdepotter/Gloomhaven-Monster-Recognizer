// Fill out your copyright notice in the Description page of Project Settings.

#include "Tile.h"
#include "TileSpawner.h"
#include "Math/UnrealMathUtility.h"
#include "Kismet/GameplayStatics.h"

// Sets default values
ATileSpawner::ATileSpawner()
{
 	// Set this actor to call Tick() every frame.  You can turn this off to improve performance if you don't need it.
	PrimaryActorTick.bCanEverTick = false;
}

// Called when the game starts or when spawned
void ATileSpawner::BeginPlay()
{
	Super::BeginPlay();

	UGameplayStatics::GetAllActorsOfClass(GetWorld(), ATile::StaticClass(), AllTiles);
}

ATile* ATileSpawner::SpawnTile()
{
	if (CurrentTile)
	{
		CurrentTile->SetActorLocation(FVector(0, 0, -1000));
	}

	CurrentTile = Cast<ATile>(AllTiles[FMath::RandRange(0, AllTiles.Num() - 1)]);

	FVector Offset = FVector(
		FMath::RandRange(-XOffsetMax, XOffsetMax),
		FMath::RandRange(-YOffsetMax, YOffsetMax),
		FMath::RandRange(-ZOffsetMax, ZOffsetMax)
	);
	CurrentTile->SetActorLocation(GetActorLocation() + Offset);
	CurrentTile->SetActorRotation(
		FRotator(0, FMath::RandRange(0, 360), 0)
	);

	return CurrentTile;
}
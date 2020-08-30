// Fill out your copyright notice in the Description page of Project Settings.

#pragma once

#include "CoreMinimal.h"
#include "GameFramework/Actor.h"
#include "TileSpawner.generated.h"

class ATile;

UCLASS()
class GLOOMHAVENRECO_API ATileSpawner : public AActor
{
	GENERATED_BODY()
	
public:	
	// Sets default values for this actor's properties
	ATileSpawner();

	UFUNCTION(BlueprintCallable)
	ATile* SpawnTile();

protected:
	// Called when the game starts or when spawned
	virtual void BeginPlay() override;

private:
	TArray<AActor*> AllTiles;

	ATile* CurrentTile = nullptr;

	UPROPERTY(EditAnywhere, Category = "Setup")
	float XOffsetMax = 50.f;
	UPROPERTY(EditAnywhere, Category = "Setup")
	float YOffsetMax = 50.f;
	UPROPERTY(EditAnywhere, Category = "Setup")
	float ZOffsetMax = 0.f;
};

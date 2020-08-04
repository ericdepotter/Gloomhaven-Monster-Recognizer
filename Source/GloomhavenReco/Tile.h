// Fill out your copyright notice in the Description page of Project Settings.

#pragma once

#include "CoreMinimal.h"
#include "GameFramework/Actor.h"
#include "Tile.generated.h"

class USpawnLocation;
class UStaticMeshComponent;

UCLASS()
class GLOOMHAVENRECO_API ATile : public AActor
{
	GENERATED_BODY()
	
public:	
	// Sets default values for this actor's properties
	ATile();

	UFUNCTION(BlueprintCallable)
	TArray<USpawnLocation*> GetSpawnLocations() const;

	UFUNCTION(BlueprintCallable)
	void PopulateTile(FVector CameraPosition, int NumberMonsters = 2);

protected:
	// Called when the game starts or when spawned
	virtual void BeginPlay() override;

private:
	UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = Setup, meta = (AllowPrivateAccess = "true"))
	UStaticMeshComponent* StaticMeshComponent = nullptr;

};

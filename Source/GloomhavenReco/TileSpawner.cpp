// Fill out your copyright notice in the Description page of Project Settings.

#include "Tile.h"
#include "TileSpawner.h"

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
	
	for(TObjectIterator<UClass> It; It; ++It)
	{
		if(It->IsChildOf(USomeAwesomeClass::StaticClass()) && !It->HasAnyClassFlags(CLASS_Abstract))
		{
			Subclasses.Add(*It);
		}
	}
}


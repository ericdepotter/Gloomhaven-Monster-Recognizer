// Fill out your copyright notice in the Description page of Project Settings.

#include "MyGameModeBase.h"
#include "Kismet/GameplayStatics.h"
#include "Monster.h"

// Sets default values
AMonster::AMonster()
{
 	// Set this actor to call Tick() every frame.  You can turn this off to improve performance if you don't need it.
	PrimaryActorTick.bCanEverTick = _CMP_FALSE_OS;

}

// Called when the game starts or when spawned
void AMonster::BeginPlay()
{
	Super::BeginPlay();
	
	GameMode = Cast<AMyGameModeBase>(UGameplayStatics::GetGameMode(GetWorld()));
	if (!GameMode)
	{
		UE_LOG(LogTemp, Error, TEXT("%s could not load game mode"), *GetName());
		return;
	}
	MonsterName = GameMode->GetRandomMonsterName();
	SwitchToTexture();
}

// Fill out your copyright notice in the Description page of Project Settings.

#pragma once

#include "CoreMinimal.h"
#include "GameFramework/Actor.h"
#include "Monster.generated.h"

class AMyGameModeBase;

UCLASS()
class GLOOMHAVENRECO_API AMonster : public AActor
{
	GENERATED_BODY()
	
public:	
	// Sets default values for this actor's properties
	AMonster();

	UFUNCTION(BlueprintImplementableEvent, BlueprintCallable)
	void SwitchToTexture();

	UFUNCTION(BlueprintImplementableEvent, BlueprintCallable)
	void SwitchToMask();

protected:
	// Called when the game starts or when spawned
	virtual void BeginPlay() override;

private:
	UPROPERTY(BlueprintReadOnly, meta = (AllowPrivateAccess = "true"))
	AMyGameModeBase* GameMode;

	UPROPERTY(BlueprintReadOnly, meta = (AllowPrivateAccess = "true"))
	FString MonsterName;

	UPROPERTY(BlueprintReadWrite, meta = (AllowPrivateAccess = "true"))
	bool bIsElite;
};

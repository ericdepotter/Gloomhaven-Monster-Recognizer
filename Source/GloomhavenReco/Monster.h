// Fill out your copyright notice in the Description page of Project Settings.

#pragma once

#include "CoreMinimal.h"
#include "GameFramework/Actor.h"
#include "Monster.generated.h"

class APlayerController;
class AMyGameModeBase;
class UStaticMeshComponent;

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

	UFUNCTION(BlueprintImplementableEvent, BlueprintCallable)
	void SwitchToBlack();

	UFUNCTION(BlueprintCallable)
	FBox2D GetScreenBoundingBox() const; 

	FString GetMonsterName() const;

protected:
	// Called when the game starts or when spawned
	virtual void BeginPlay() override;

private:
	UPROPERTY(EditAnywhere, BlueprintReadWrite, meta = (AllowPrivateaccess = "true"))
	UStaticMeshComponent* Standee = nullptr;

	UPROPERTY(EditAnywhere, BlueprintReadWrite, meta = (AllowPrivateaccess = "true"))
	UStaticMeshComponent* Monster = nullptr;

	UPROPERTY(BlueprintReadOnly, meta = (AllowPrivateAccess = "true"))
	AMyGameModeBase* GameMode;

	APlayerController* PlayerController = nullptr;

	UPROPERTY(BlueprintReadOnly, meta = (AllowPrivateAccess = "true"))
	FString MonsterName;

	UPROPERTY(BlueprintReadWrite, meta = (AllowPrivateAccess = "true"))
	bool bIsElite;
};

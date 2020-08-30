// Fill out your copyright notice in the Description page of Project Settings.

#pragma once

#include "CoreMinimal.h"
#include "GameFramework/GameModeBase.h"
#include "MyGameModeBase.generated.h"

/**
 * 
 */
UCLASS()
class GLOOMHAVENRECO_API AMyGameModeBase : public AGameModeBase
{
	GENERATED_BODY()
	
public:
	virtual void InitGame(const FString& MapName, const FString& Options, FString& ErrorMessage) override;

	//static TArray<FAssetData> DynamicLoadContentFromPath(FString PathFromContentFolder, bool LoadFromSubfolders);

	FString GetRandomMonsterName() const;
	UFUNCTION(BlueprintCallable)
	UTexture2D* GetMonsterTexture(FString MonsterName) const;
	UFUNCTION(BlueprintCallable)
	UTexture2D* GetMonsterMask(FString MonsterName) const;

protected:
	UFUNCTION(BlueprintImplementableEvent)
	void LoadMonsterTexturesAndMasks();

private:
	UPROPERTY(BlueprintReadWrite, Category = "Monsters", meta = (AllowPrivateAccess = "true"))
	TSet<FString> MonsterNames;
	UPROPERTY(BlueprintReadWrite, Category = "Monsters", meta = (AllowPrivateAccess = "true"))
	TMap<FString, UTexture2D*> MonsterTextures;
	UPROPERTY(BlueprintReadWrite, Category = "Monsters", meta = (AllowPrivateAccess = "true"))
	TMap<FString, UTexture2D*> MonsterMasks;


};

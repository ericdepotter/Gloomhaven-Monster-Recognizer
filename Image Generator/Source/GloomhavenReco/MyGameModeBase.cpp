// Fill out your copyright notice in the Description page of Project Settings.

#include "MyGameModeBase.h"
#include "Modules/ModuleManager.h"
#include "AssetRegistryModule.h"
#include "AssetData.h"


/*TArray<FAssetData> AMyGameModeBase::DynamicLoadContentFromPath(FString PathFromContentFolder, bool LoadFromSubfolders) 
{
    TArray<FAssetData> AssetData;
    FAssetRegistryModule& AssetRegistryModule = FModuleManager::LoadModuleChecked<FAssetRegistryModule>("AssetRegistry");
    AssetRegistryModule.Get().GetAssetsByPath("/Game/Monsters/Materials", AssetData);

    return AssetData;
}*/

void AMyGameModeBase::InitGame(const FString& MapName, const FString& Options, FString& ErrorMessage) 
{
    Super::InitGame(MapName, Options, ErrorMessage);

    LoadMonsterTexturesAndMasks();
    /*TArray<FAssetData> MonsterTextureAssets = AMyGameModeBase::DynamicLoadContentFromPath("Monsters/Materials", false);
    UE_LOG(LogTemp, Warning, TEXT("Monsters found: %s"), MonsterTextures.Num());

    for (FAssetData AssetData: MonsterTextureAssets)
    {
        UE_LOG(LogTemp, Warning, TEXT("%s: %s"), *AssetData.AssetName.ToString(), *AssetData.AssetClass.ToString());
    }*/
}


FString AMyGameModeBase::GetRandomMonsterName() const
{
    return MonsterNames.Array()[FMath::RandRange(0, MonsterNames.Num() - 1)];
}

UTexture2D* AMyGameModeBase::GetMonsterTexture(FString MonsterName) const
{
    return MonsterTextures[MonsterName];
}

UTexture2D* AMyGameModeBase::GetMonsterMask(FString MonsterName) const
{
    return MonsterMasks[MonsterName];
}
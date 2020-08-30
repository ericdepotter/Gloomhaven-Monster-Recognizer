// Fill out your copyright notice in the Description page of Project Settings.


#include "UTextFileManager.h"
#include "Misc/FileHelper.h"
#include "HAL/PlatformFilemanager.h"

bool UUTextFileManager::SaveArrayText(FString SaveDirectory, FString Filename, TArray<FString> SaveText, bool bAllowOverriding) 
{
    // Set complete file path
    SaveDirectory += "\\" + Filename;

    if (!bAllowOverriding && FPlatformFileManager::Get().GetPlatformFile().FileExists(*SaveDirectory))
    {
        return false;
    }

    return FFileHelper::SaveStringArrayToFile(SaveText, *SaveDirectory);
}

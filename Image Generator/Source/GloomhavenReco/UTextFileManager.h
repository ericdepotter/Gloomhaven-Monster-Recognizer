// Fill out your copyright notice in the Description page of Project Settings.

#pragma once

#include "CoreMinimal.h"
#include "Kismet/BlueprintFunctionLibrary.h"
#include "UTextFileManager.generated.h"

/**
 * https://www.youtube.com/watch?v=uZPzTN5Debc
 */
UCLASS()
class GLOOMHAVENRECO_API UUTextFileManager : public UBlueprintFunctionLibrary
{
	GENERATED_BODY()
	
	UFUNCTION(BlueprintCallable, Category = Custom, meta = (Keywords = "Save"))
	static bool SaveArrayText(FString SaveDirectory, FString Filename, TArray<FString> SaveText, bool bAllowOverriding);
};

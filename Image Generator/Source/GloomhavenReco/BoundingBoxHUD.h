// Fill out your copyright notice in the Description page of Project Settings.

#pragma once

#include "CoreMinimal.h"
#include "GameFramework/HUD.h"
#include "BoundingBoxHUD.generated.h"

struct FBox2D;

/**
 * 
 */
UCLASS()
class GLOOMHAVENRECO_API ABoundingBoxHUD : public AHUD
{
	GENERATED_BODY()

public:
	UFUNCTION(BlueprintCallable)
	bool AddBoundingBox(FBox2D BoundingBox);

	virtual void DrawHUD() override;

private:
	TArray<FBox2D> BoundingBoxesToDraw;
};

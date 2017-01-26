/*
 * relays.c
 *
 *  Created on: Jan 26, 2017
 *      Author: Derryn Harvie
 */

#include "relays.h"
#include "stm32f10x_rcc.h"
#include "stm32f10x_gpio.h"

uint8_t relayOffDelayCounter = 0;
uint8_t relayNumberToSwitchOn = 0;
uint8_t relaySwitchOnDelayTimeOut = 0;

void relaysInit(void)
{
	RCC_APB2PeriphClockCmd(RCC_APB2Periph_GPIOA, ENABLE);
	RCC_APB2PeriphClockCmd(RCC_APB2Periph_GPIOB, ENABLE);

	GPIO_InitTypeDef GPIO_InitStruct;
	GPIO_InitStruct.GPIO_Pin = 0x3FF;
	GPIO_InitStruct.GPIO_Mode = GPIO_Mode_Out_PP;
	GPIO_InitStruct.GPIO_Speed = GPIO_Speed_2MHz;
	GPIO_Init(GPIOA, &GPIO_InitStruct);

	GPIO_ResetBits(GPIOA, 0x3FF);

	GPIO_InitStruct.GPIO_Pin = GPIO_Pin_0 | GPIO_Pin_1;
	GPIO_Init(GPIOB, &GPIO_InitStruct);
	GPIO_ResetBits(GPIOB, GPIO_Pin_0 | GPIO_Pin_1);

}

// Called every ms to time relay switching
void relayTick(void) {
	if (relayOffDelayCounter != 0) {
		GPIO_SetBits(GPIOB, GPIO_Pin_1);
		relayOffDelayCounter--;
	} else if (relayNumberToSwitchOn != 0) {
		if (relayNumberToSwitchOn <= 10 && relayNumberToSwitchOn >= 1) {
			uint8_t gpioPinNumber = relayNumberToSwitchOn - 1;
			GPIO_SetBits(GPIOA, (1 << gpioPinNumber));
		}
		relayNumberToSwitchOn = 0;
		relaySwitchOnDelayTimeOut = 2;
	} else if( relaySwitchOnDelayTimeOut != 0)
	{
		relaySwitchOnDelayTimeOut--;
		if(relaySwitchOnDelayTimeOut == 0)
		{
			GPIO_SetBits(GPIOB, GPIO_Pin_0);
		}
	} else {
		GPIO_ResetBits(GPIOB, GPIO_Pin_0 | GPIO_Pin_1);
	}

}

void relaysOff(void)
{
	GPIO_ResetBits(GPIOA, 0x3FF);
	relayOffDelayCounter = 3; // Guarantee at least 2ms before switching on another relay
}

void relayOn(uint8_t relayNumber)
{
	relaysOff();
	relayNumberToSwitchOn = relayNumber; // Hold relay number for when delay has complete.
}

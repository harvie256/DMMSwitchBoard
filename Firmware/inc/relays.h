/*
 * relays.h
 *
 *  Created on: Jan 26, 2017
 *      Author: Derryn Harvie
 */

#ifndef RELAYS_H_
#define RELAYS_H_

#include "platform_config.h"

void relaysOff(void);
void relayOn(uint8_t relayNumber);
void relaysInit(void);
void relayTick(void);

#endif /* RELAYS_H_ */

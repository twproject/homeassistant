"""Support for Modbus."""
from __future__ import annotations

import logging
from typing import cast

import voluptuous as vol

from homeassistant.const import (
    CONF_ADDRESS,
    CONF_BINARY_SENSORS,
    CONF_COMMAND_OFF,
    CONF_COMMAND_ON,
    CONF_COUNT,
    CONF_COVERS,
    CONF_DELAY,
    CONF_DEVICE_CLASS,
    CONF_HOST,
    CONF_LIGHTS,
    CONF_METHOD,
    CONF_NAME,
    CONF_OFFSET,
    CONF_PORT,
    CONF_SCAN_INTERVAL,
    CONF_SENSORS,
    CONF_SLAVE,
    CONF_STRUCTURE,
    CONF_SWITCHES,
    CONF_TEMPERATURE_UNIT,
    CONF_TIMEOUT,
    CONF_TYPE,
    CONF_UNIQUE_ID,
    CONF_UNIT_OF_MEASUREMENT,
)
from homeassistant.core import HomeAssistant
import homeassistant.helpers.config_validation as cv
from homeassistant.helpers.typing import ConfigType

from .const import (  # noqa: F401
    CALL_TYPE_COIL,
    CALL_TYPE_DISCRETE,
    CALL_TYPE_REGISTER_HOLDING,
    CALL_TYPE_REGISTER_INPUT,
    CALL_TYPE_WRITE_REGISTER,
    CALL_TYPE_X_COILS,
    CALL_TYPE_X_REGISTER_HOLDINGS,
    CONF_BAUDRATE,
    CONF_BYTESIZE,
    CONF_CLIMATES,
    CONF_CLOSE_COMM_ON_ERROR,
    CONF_DATA_TYPE,
    CONF_FANS,
    CONF_HUB,
    CONF_HVAC_MODE_AUTO,
    CONF_HVAC_MODE_COOL,
    CONF_HVAC_MODE_DRY,
    CONF_HVAC_MODE_FAN_ONLY,
    CONF_HVAC_MODE_HEAT,
    CONF_HVAC_MODE_HEAT_COOL,
    CONF_HVAC_MODE_OFF,
    CONF_HVAC_MODE_REGISTER,
    CONF_HVAC_MODE_VALUES,
    CONF_HVAC_ONOFF_REGISTER,
    CONF_HUMIDITY_REGISTER,
    CONF_INPUT_TYPE,
    CONF_LAZY_ERROR,
    CONF_MAX_TEMP,
    CONF_MAX_VALUE,
    CONF_MIN_TEMP,
    CONF_MIN_VALUE,
    CONF_MSG_WAIT,
    CONF_PARITY,
    CONF_PRECISION,
    CONF_RETRIES,
    CONF_RETRY_ON_EMPTY,
    CONF_SCALE,
    CONF_SLAVE_COUNT,
    CONF_STATE_CLOSED,
    CONF_STATE_CLOSING,
    CONF_STATE_OFF,
    CONF_STATE_ON,
    CONF_STATE_OPEN,
    CONF_STATE_OPENING,
    CONF_STATUS_REGISTER,
    CONF_STATUS_REGISTER_TYPE,
    CONF_STEP,
    CONF_STOPBITS,
    CONF_SWAP,
    CONF_SWAP_BYTE,
    CONF_SWAP_NONE,
    CONF_SWAP_WORD,
    CONF_SWAP_WORD_BYTE,
    CONF_TARGET_TEMP,
    CONF_VERIFY,
    CONF_WRITE_REGISTERS,
    CONF_WRITE_TYPE,
    CONF_ZERO_SUPPRESS,
    DEFAULT_HUB,
    DEFAULT_SCAN_INTERVAL,
    DEFAULT_TEMP_UNIT,
    MODBUS_DOMAIN as DOMAIN,
    RTUOVERTCP,
    SERIAL,
    TCP,
    UDP,
    DataType,
)
from .modbus import ModbusHub, async_modbus_setup
from .validators import (
    duplicate_entity_validator,
    duplicate_modbus_validator,
    number_validator,
    scan_interval_validator,
    struct_validator,
)

_LOGGER = logging.getLogger(__name__)


BASE_SCHEMA = vol.Schema({vol.Optional(CONF_NAME, default=DEFAULT_HUB): cv.string})


BASE_COMPONENT_SCHEMA = vol.Schema(
    {
        vol.Required(CONF_NAME): cv.string,
        vol.Required(CONF_ADDRESS): cv.positive_int,
        vol.Optional(CONF_SLAVE, default=0): cv.positive_int,
        vol.Optional(
            CONF_SCAN_INTERVAL, default=DEFAULT_SCAN_INTERVAL
        ): cv.positive_int,
        vol.Optional(CONF_LAZY_ERROR, default=0): cv.positive_int,
        vol.Optional(CONF_UNIQUE_ID): cv.string,
    }
)


BASE_STRUCT_SCHEMA = BASE_COMPONENT_SCHEMA.extend(
    {
        vol.Optional(CONF_INPUT_TYPE, default=CALL_TYPE_REGISTER_HOLDING): vol.In(
            [
                CALL_TYPE_REGISTER_HOLDING,
                CALL_TYPE_REGISTER_INPUT,
            ]
        ),
        vol.Optional(CONF_COUNT): cv.positive_int,
        vol.Optional(CONF_DATA_TYPE, default=DataType.INT16): vol.In(
            [
                DataType.INT8,
                DataType.INT16,
                DataType.INT32,
                DataType.INT64,
                DataType.UINT8,
                DataType.UINT16,
                DataType.UINT32,
                DataType.UINT64,
                DataType.FLOAT16,
                DataType.FLOAT32,
                DataType.FLOAT64,
                DataType.STRING,
                DataType.STRING,
                DataType.CUSTOM,
            ]
        ),
        vol.Optional(CONF_STRUCTURE): cv.string,
        vol.Optional(CONF_SCALE, default=1): number_validator,
        vol.Optional(CONF_OFFSET, default=0): number_validator,
        vol.Optional(CONF_PRECISION, default=0): cv.positive_int,
        vol.Optional(CONF_SWAP, default=CONF_SWAP_NONE): vol.In(
            [
                CONF_SWAP_NONE,
                CONF_SWAP_BYTE,
                CONF_SWAP_WORD,
                CONF_SWAP_WORD_BYTE,
            ]
        ),
    }
)

CLIMATE_SCHEMA = vol.All(
    BASE_STRUCT_SCHEMA.extend(
        {
            vol.Required(CONF_TARGET_TEMP): cv.positive_int,
            vol.Optional(CONF_MAX_TEMP, default=35): cv.positive_int,
            vol.Optional(CONF_MIN_TEMP, default=5): cv.positive_int,
            vol.Optional(CONF_STEP, default=0.5): vol.Coerce(float),
            vol.Optional(CONF_TEMPERATURE_UNIT, default=DEFAULT_TEMP_UNIT): cv.string,
            vol.Optional(CONF_HVAC_ONOFF_REGISTER): cv.positive_int,
            vol.Optional(CONF_HUMIDITY_REGISTER): cv.positive_int,
            vol.Optional(CONF_WRITE_REGISTERS, default=False): cv.boolean,
            vol.Optional(CONF_HVAC_MODE_REGISTER): vol.Maybe(
                {
                    CONF_ADDRESS: cv.positive_int,
                    CONF_HVAC_MODE_VALUES: {
                        vol.Optional(CONF_HVAC_MODE_OFF): cv.positive_int,
                        vol.Optional(CONF_HVAC_MODE_HEAT): cv.positive_int,
                        vol.Optional(CONF_HVAC_MODE_COOL): cv.positive_int,
                        vol.Optional(CONF_HVAC_MODE_HEAT_COOL): cv.positive_int,
                        vol.Optional(CONF_HVAC_MODE_AUTO): cv.positive_int,
                        vol.Optional(CONF_HVAC_MODE_DRY): cv.positive_int,
                        vol.Optional(CONF_HVAC_MODE_FAN_ONLY): cv.positive_int,
                    },
                    vol.Optional(CONF_WRITE_REGISTERS, default=False): cv.boolean,
                }
            ),
        }
    ),
)



MODBUS_SCHEMA = vol.Schema(
    {
        vol.Optional(CONF_NAME, default=DEFAULT_HUB): cv.string,
        vol.Optional(CONF_TIMEOUT, default=3): cv.socket_timeout,
        vol.Optional(CONF_CLOSE_COMM_ON_ERROR, default=True): cv.boolean,
        vol.Optional(CONF_DELAY, default=0): cv.positive_int,
        vol.Optional(CONF_RETRIES, default=3): cv.positive_int,
        vol.Optional(CONF_RETRY_ON_EMPTY, default=False): cv.boolean,
        vol.Optional(CONF_MSG_WAIT): cv.positive_int,
        vol.Optional(CONF_CLIMATES): vol.All(
            cv.ensure_list, [vol.All(CLIMATE_SCHEMA, struct_validator)]
        ),
    }
)

SERIAL_SCHEMA = MODBUS_SCHEMA.extend(
    {
        vol.Required(CONF_TYPE): SERIAL,
        vol.Required(CONF_BAUDRATE): cv.positive_int,
        vol.Required(CONF_BYTESIZE): vol.Any(5, 6, 7, 8),
        vol.Required(CONF_METHOD): vol.Any("rtu", "ascii"),
        vol.Required(CONF_PORT): cv.string,
        vol.Required(CONF_PARITY): vol.Any("E", "O", "N"),
        vol.Required(CONF_STOPBITS): vol.Any(1, 2),
    }
)

ETHERNET_SCHEMA = MODBUS_SCHEMA.extend(
    {
        vol.Required(CONF_HOST): cv.string,
        vol.Required(CONF_PORT): cv.port,
        vol.Required(CONF_TYPE): vol.Any(TCP, UDP, RTUOVERTCP),
    }
)

CONFIG_SCHEMA = vol.Schema(
    {
        DOMAIN: vol.All(
            cv.ensure_list,
            scan_interval_validator,
            duplicate_entity_validator,
            duplicate_modbus_validator,
            [
                vol.Any(SERIAL_SCHEMA, ETHERNET_SCHEMA),
            ],
        ),
    },
    extra=vol.ALLOW_EXTRA,
)


def get_hub(hass: HomeAssistant, name: str) -> ModbusHub:
    """Return modbus hub with name."""
    return cast(ModbusHub, hass.data[DOMAIN][name])


async def async_setup(hass: HomeAssistant, config: ConfigType) -> bool:
    """Set up Modbus component."""
    if DOMAIN not in config:
        return True
    return await async_modbus_setup(
        hass,
        config,
    )


async def async_reset_platform(hass: HomeAssistant, integration_name: str) -> None:
    """Release modbus resources."""
    _LOGGER.info("Modbus reloading")
    hubs = hass.data[DOMAIN]
    for name in hubs:
        await hubs[name].async_close()

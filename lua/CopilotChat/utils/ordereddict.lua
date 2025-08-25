---@class OrderedDict<K, V>
---@field set fun(self:OrderedDict, key:any, value:any)
---@field get fun(self:OrderedDict, key:any):any
---@field keys fun(self:OrderedDict):table
---@field values fun(self:OrderedDict):table

--- Create an ordered dict
---@generic K, V
---@return OrderedDict<K, V>
local function ordereddict()
  return {
    _keys = {},
    _data = {},
    set = function(self, key, value)
      if not self._data[key] then
        table.insert(self._keys, key)
      end
      self._data[key] = value
    end,

    get = function(self, key)
      return self._data[key]
    end,

    keys = function(self)
      return self._keys
    end,

    values = function(self)
      local result = {}
      for _, key in ipairs(self._keys) do
        table.insert(result, self._data[key])
      end
      return result
    end,
  }
end

return ordereddict

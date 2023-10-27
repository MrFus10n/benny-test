import * as mui from '@mui/material'
import React from 'react'

import * as api from 'api/api'
import { ParserConditions } from 'api/models'
import { testInputs } from './TestInputs'


function ConditionsTable({conditions}: {conditions: ParserConditions}) {
  return (
    <mui.Table sx={{ border: '1px solid grey' }}>
      <mui.TableBody>
        {conditions.periods.map((period, i) => (
          <mui.TableRow key={i}>
            <mui.TableCell>Period {i}</mui.TableCell>
            <mui.TableCell>{period.start} - {period.end}</mui.TableCell>
          </mui.TableRow>
        ))}
        <mui.TableRow>
          <mui.TableCell>Min amount</mui.TableCell>
          <mui.TableCell>{conditions.amount_min}</mui.TableCell>
        </mui.TableRow>
        <mui.TableRow>
          <mui.TableCell>Max amount</mui.TableCell>
          <mui.TableCell>{conditions.amount_max}</mui.TableCell>
        </mui.TableRow>
      </mui.TableBody>
    </mui.Table>
  )
}


export function Parser() {
  const [conditions, setConditions] = React.useState<ParserConditions>()
  const [text, setText] = React.useState('')
  const parser = api.useRunParser(
    {axios: {headers: {'X-CSRFToken': window.GLOBAL_CONFIG.CSRF}}}  // TODO: This should be encapsulated
  )

  function handleParse() {
    parser
    .mutateAsync({data: {text}})
    .then(res => {setConditions(res.data.conditions)})
  }

  function handleTextChange(e: React.ChangeEvent<HTMLInputElement>) {
    setConditions(undefined)
    setText(e.target.value)
  }

  return (
    <mui.Box display="flex" alignItems="center" flexDirection="column" pt={5}>

      {conditions && <ConditionsTable conditions={conditions}/>}

      <mui.Box display="flex" alignItems="center">
        {testInputs.map((input, i) => (
          <mui.Button
            onClick={() => setText(testInputs[i])}
            variant="outlined"
            sx={{m: 2}}
            key={i}
          >
            Use test #{i}
          </mui.Button>
        ))}
        <mui.Button
          onClick={handleParse}
          variant="contained"
          color="success"
          disabled={!text}
          sx={{m: 2}}
        >
          Parse
        </mui.Button>
      </mui.Box>

      <mui.TextField
        label="Text Input"
        variant="outlined"
        multiline
        rows={15}
        fullWidth
        sx={{mb: 20}}
        value={text}
        onChange={handleTextChange}
      />
    </mui.Box>
  )
}

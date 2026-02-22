import copy

def safe_execute(df, code):
    df_backup = copy.deepcopy(df)
    local_env = {"df": df}

    try:
        exec(code, {}, local_env)
        return local_env["df"], None
    except Exception as e:
        return df_backup, str(e)
